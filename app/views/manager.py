from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.decorators import role_required
from app.extensions import db
from app.forms.manager_forms import SubmissionReviewForm
from app.models import BalanceType, Project, Role, Submission, SubmissionStatus

manager_bp = Blueprint("manager", __name__, url_prefix="/manager")


@manager_bp.before_request
@login_required
def ensure_manager():
    if current_user.role not in (Role.MANAGER, Role.ADMIN):
        abort(403)


@manager_bp.route("/projects")
def managed_projects():
    projects = Project.query.filter_by(manager_id=current_user.id).order_by(Project.created_at.desc()).all()
    return render_template("manager/projects.html", projects=projects)


@manager_bp.route("/projects/<int:project_id>/submissions")
def project_submissions(project_id: int):
    project = Project.query.get_or_404(project_id)
    if project.manager_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)
    submissions = Submission.query.filter_by(project_id=project_id).order_by(Submission.created_at.desc()).all()
    return render_template("manager/submissions.html", project=project, submissions=submissions)


@manager_bp.route("/submissions/<int:submission_id>", methods=["GET", "POST"])
def review_submission(submission_id: int):
    submission = Submission.query.get_or_404(submission_id)
    project = submission.project
    if project.manager_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)

    form = SubmissionReviewForm(obj=submission)
    if form.validate_on_submit():
        new_status = SubmissionStatus(form.status.data)
        if new_status == SubmissionStatus.REJECTED and not form.reject_reason.data:
            flash("Provide a reason when rejecting", "warning")
            return render_template("manager/review.html", submission=submission, project=project, form=form)

        submission.views = form.views.data
        submission.status = new_status
        submission.reject_reason = form.reject_reason.data.strip() if form.reject_reason.data else None

        if new_status == SubmissionStatus.APPROVED:
            reward = project.calculate_reward(submission.views)
            submission.reward_cents = reward
            submission.clipper.adjust_balance(reward, f"Submission #{submission.id} approved", BalanceType.EARNING)
        else:
            submission.reward_cents = None

        db.session.commit()
        flash("Submission updated", "success")
        return redirect(url_for("manager.project_submissions", project_id=project.id))

    return render_template("manager/review.html", submission=submission, project=project, form=form)
