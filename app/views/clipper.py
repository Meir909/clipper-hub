from __future__ import annotations

from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import role_required
from app.extensions import db
from app.forms.payout_forms import PayoutRequestForm
from app.forms.submission_forms import SubmissionForm
from app.models import (BalanceType, PayoutRequest, PayoutStatus, PlatformType,
                        Project, ProjectAccess, Role, Submission,
                        SubmissionStatus)

clipper_bp = Blueprint("clipper", __name__, url_prefix="/clipper")

DAILY_SUBMISSION_LIMIT = 10
MIN_PAYOUT_CENTS = 2000  # 20 euros


def _ensure_clipper():
    if current_user.role != Role.CLIPPER:
        abort(403)


def _submission_limit_reached() -> bool:
    today_start = datetime.combine(datetime.utcnow().date(), datetime.min.time())
    today_count = Submission.query.filter(
        Submission.clipper_id == current_user.id,
        Submission.created_at >= today_start,
    ).count()
    return today_count >= DAILY_SUBMISSION_LIMIT


@clipper_bp.before_request
@login_required
def before_request():
    _ensure_clipper()


@clipper_bp.route("/projects")
def projects():
    query = Project.query.filter(Project.access_mode == ProjectAccess.OPEN)
    query = query.order_by(Project.created_at.desc())
    projects = [p for p in query.all() if p.is_active()]
    return render_template("clipper/projects.html", projects=projects)


@clipper_bp.route("/projects/<int:project_id>")
def project_detail(project_id: int):
    project = Project.query.get_or_404(project_id)
    if project.access_mode != ProjectAccess.OPEN:
        abort(403)
    return render_template("clipper/project_detail.html", project=project)


@clipper_bp.route("/projects/<int:project_id>/submit", methods=["GET", "POST"])
def submit_video(project_id: int):
    project = Project.query.get_or_404(project_id)
    if project.access_mode != ProjectAccess.OPEN:
        abort(403)

    form = SubmissionForm()
    if form.validate_on_submit():
        if _submission_limit_reached():
            flash("Daily submission limit reached (10). Try tomorrow.", "warning")
            return redirect(url_for("clipper.project_detail", project_id=project_id))

        if project.submission_limit_per_user:
            per_project_count = Submission.query.filter_by(
                project_id=project.id,
                clipper_id=current_user.id,
            ).count()
            if per_project_count >= project.submission_limit_per_user:
                flash("Project submission limit reached for you.", "warning")
                return redirect(url_for("clipper.project_detail", project_id=project_id))

        submission = Submission(
            project=project,
            clipper=current_user,
            video_url=form.video_url.data.strip(),
            platform=PlatformType(form.platform.data),
        )
        db.session.add(submission)
        db.session.commit()
        flash("Submission sent for review.", "success")
        return redirect(url_for("clipper.my_submissions"))

    return render_template("clipper/submit.html", form=form, project=project)


@clipper_bp.route("/submissions")
def my_submissions():
    submissions = Submission.query.filter_by(clipper_id=current_user.id).order_by(Submission.created_at.desc()).all()
    return render_template("clipper/submissions.html", submissions=submissions)


@clipper_bp.route("/payout", methods=["GET", "POST"])
def request_payout():
    form = PayoutRequestForm()
    current_balance = current_user.balance_cents

    if form.validate_on_submit():
        euro_value = form.amount.data or 0
        amount_cents = int(euro_value * 100)
        if amount_cents < MIN_PAYOUT_CENTS:
            flash("Minimum payout is €20", "warning")
            return render_template("clipper/payout.html", form=form, balance=current_balance)
        if amount_cents > current_balance:
            flash("You cannot request more than your balance", "danger")
            return render_template("clipper/payout.html", form=form, balance=current_balance)

        payout = PayoutRequest(
            user=current_user,
            amount_cents=amount_cents,
            method=form.method.data,
            details=form.details.data.strip(),
        )
        current_user.adjust_balance(-amount_cents, "Payout requested", BalanceType.PAYOUT)
        db.session.add(payout)
        db.session.commit()
        flash("Payout request submitted", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("clipper/payout.html", form=form, balance=current_balance)
