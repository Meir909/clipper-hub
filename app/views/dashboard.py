from __future__ import annotations

from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import (PayoutRequest, PayoutStatus, Project, ProjectAccess,
                        Role, Submission, SubmissionStatus, User)


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def landing():
    return render_template("landing.html")


@dashboard_bp.route("/dashboard")
@login_required
def index():
    role_value = current_user.role.value
    context = {"role": role_value}

    if current_user.role == Role.ADMIN:
        context.update(
            total_projects=Project.query.count(),
            total_clippers=User.query.filter_by(role=Role.CLIPPER).count(),
            pending_payouts=PayoutRequest.query.filter_by(status=PayoutStatus.PENDING).count(),
        )
    elif current_user.role == Role.MANAGER:
        pending = Submission.query.join(Project).filter(
            Project.manager_id == current_user.id,
            Submission.status == SubmissionStatus.PENDING,
        ).all()
        context.update(pending_submissions=pending)
    else:
        latest_projects = (
            Project.query
            .filter(Project.access_mode == ProjectAccess.OPEN)
            .order_by(Project.created_at.desc())
            .limit(6)
            .all()
        )
        today = datetime.utcnow().date()
        today_count = Submission.query.filter(
            Submission.clipper_id == current_user.id,
            Submission.created_at >= datetime.combine(today, datetime.min.time()),
        ).count()
        context.update(
            latest_projects=latest_projects,
            today_submissions=today_count,
        )

    return render_template("dashboard/index.html", **context)
