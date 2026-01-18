from __future__ import annotations

from flask import Blueprint, abort, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms.admin_forms import CreateUserForm, PayoutDecisionForm, UserRoleForm
from app.forms.project_forms import ProjectForm
from app.models import (PayoutRequest, PayoutStatus, PaymentType, Project,
                        ProjectAccess, Role, User)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
@login_required
def ensure_admin():
    if current_user.role != Role.ADMIN:
        abort(403)


@admin_bp.route("/users", methods=["GET", "POST"])
def users():
    create_form = CreateUserForm()
    users = User.query.order_by(User.created_at.desc()).all()
    if create_form.validate_on_submit():
        desired_role = Role(create_form.role.data)
        if desired_role == Role.ADMIN and create_form.email.data.lower() not in current_app.config["ADMIN_EMAIL_ALLOWLIST"]:
            flash("This email is not allowed to become admin", "danger")
            return render_template("admin/users.html", users=users, form=create_form, role_forms={user.id: UserRoleForm(role=user.role.value) for user in users})
        if User.query.filter_by(email=create_form.email.data.lower()).first():
            flash("Email already exists", "warning")
        else:
            user = User(
                email=create_form.email.data.lower(),
                role=desired_role,
                display_name=create_form.display_name.data or None,
            )
            user.set_password(create_form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User created", "success")
            return redirect(url_for("admin.users"))
    role_forms = {user.id: UserRoleForm(role=user.role.value) for user in users}
    return render_template("admin/users.html", users=users, form=create_form, role_forms=role_forms)


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
def update_user_role(user_id: int):
    user = User.query.get_or_404(user_id)
    form = UserRoleForm()
    if form.validate_on_submit():
        new_role = Role(form.role.data)
        if new_role == Role.ADMIN and user.email.lower() not in current_app.config["ADMIN_EMAIL_ALLOWLIST"]:
            flash("This email is not allowed to become admin", "danger")
            return redirect(url_for("admin.users"))
        user.role = new_role
        db.session.commit()
        flash("Role updated", "success")
    return redirect(url_for("admin.users"))


def _set_manager_choices(form: ProjectForm) -> None:
    managers = User.query.filter(User.role.in_([Role.MANAGER, Role.ADMIN])).all()
    form.manager_id.choices = [(-1, "Unassigned")] + [(m.id, m.display_name or m.email) for m in managers]


@admin_bp.route("/projects")
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("admin/projects.html", projects=projects)


@admin_bp.route("/projects/create", methods=["GET", "POST"])
def create_project():
    form = ProjectForm()
    _set_manager_choices(form)
    if form.validate_on_submit():
        project = Project()
        _assign_project_fields(project, form)
        db.session.add(project)
        db.session.commit()
        flash("Project created", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", form=form, title="Create project")


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)
    _set_manager_choices(form)
    if project.manager_id is None:
        form.manager_id.data = -1
    if form.validate_on_submit():
        _assign_project_fields(project, form)
        db.session.commit()
        flash("Project updated", "success")
        return redirect(url_for("admin.projects"))
    return render_template("admin/project_form.html", form=form, title="Edit project", project=project)


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id: int):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project removed", "info")
    return redirect(url_for("admin.projects"))


def _assign_project_fields(project: Project, form: ProjectForm) -> None:
    project.title = form.title.data.strip()
    project.description = form.description.data.strip()
    project.earning_conditions = form.earning_conditions.data.strip()
    project.payment_type = PaymentType(form.payment_type.data)
    project.rate_per_view_cents = form.rate_per_view_cents.data or 0
    project.fixed_reward_cents = form.fixed_reward_cents.data or 0
    project.kpi_views = form.kpi_views.data or 0
    project.instruction_url = form.instruction_url.data or None
    project.access_mode = ProjectAccess(form.access_mode.data)
    project.submission_limit_per_user = form.submission_limit_per_user.data
    project.start_date = form.start_date.data
    project.end_date = form.end_date.data
    manager_id = form.manager_id.data
    project.manager_id = None if manager_id in (None, -1) else manager_id


@admin_bp.route("/payouts", methods=["GET", "POST"])
def payouts():
    pending = PayoutRequest.query.filter_by(status=PayoutStatus.PENDING).order_by(PayoutRequest.created_at.asc()).all()
    completed = PayoutRequest.query.filter(PayoutRequest.status != PayoutStatus.PENDING).order_by(PayoutRequest.updated_at.desc()).limit(20).all()
    form = PayoutDecisionForm()
    return render_template("admin/payouts.html", pending=pending, completed=completed, form=form)


@admin_bp.route("/payouts/<int:payout_id>/confirm", methods=["POST"])
def confirm_payout(payout_id: int):
    payout = PayoutRequest.query.get_or_404(payout_id)
    if payout.status != PayoutStatus.PENDING:
        flash("Already processed", "info")
        return redirect(url_for("admin.payouts"))
    form = PayoutDecisionForm()
    if form.validate_on_submit():
        payout.status = PayoutStatus.PAID
        payout.processed_by = current_user
        db.session.commit()
        flash("Marked as paid", "success")
    return redirect(url_for("admin.payouts"))
