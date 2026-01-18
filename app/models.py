from __future__ import annotations

from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from sqlalchemy import CheckConstraint, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensions import db, bcrypt


class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CLIPPER = "clipper"


class PaymentType(str, Enum):
    FIX_PER_VIDEO = "fix_video"
    FIX_PER_PERIOD = "fix_period"
    PER_VIEW = "per_view"


class ProjectAccess(str, Enum):
    OPEN = "open"
    APPROVAL = "approval"


class SubmissionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PlatformType(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"


class PayoutStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    REJECTED = "rejected"


class BalanceType(str, Enum):
    EARNING = "earning"
    PAYOUT = "payout"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role), default=Role.CLIPPER, nullable=False)
    display_name: Mapped[str | None] = mapped_column(db.String(120))
    balance_cents: Mapped[int] = mapped_column(default=0)
    total_earned_cents: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    managed_projects: Mapped[list[Project]] = relationship("Project", back_populates="manager", cascade="all,delete", foreign_keys="Project.manager_id")
    submissions: Mapped[list[Submission]] = relationship("Submission", back_populates="clipper", foreign_keys="Submission.clipper_id")
    payout_requests: Mapped[list[PayoutRequest]] = relationship(
        "PayoutRequest",
        back_populates="user",
        foreign_keys="PayoutRequest.user_id",
        cascade="all,delete-orphan",
    )
    balance_transactions: Mapped[list[BalanceTransaction]] = relationship("BalanceTransaction", back_populates="user", cascade="all,delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def balance_eur(self) -> float:
        return self.balance_cents / 100

    def adjust_balance(self, amount_cents: int, reason: str, tx_type: BalanceType) -> None:
        self.balance_cents += amount_cents
        if tx_type == BalanceType.EARNING:
            self.total_earned_cents += amount_cents
        transaction = BalanceTransaction(
            user=self,
            amount_cents=amount_cents,
            reason=reason,
            tx_type=tx_type,
        )
        db.session.add(transaction)


class Project(db.Model):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(120), nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)
    earning_conditions: Mapped[str] = mapped_column(db.String(500), nullable=False)
    payment_type: Mapped[PaymentType] = mapped_column(SAEnum(PaymentType), nullable=False)
    rate_per_view_cents: Mapped[int | None] = mapped_column()
    fixed_reward_cents: Mapped[int | None] = mapped_column()
    kpi_views: Mapped[int | None] = mapped_column()
    instruction_url: Mapped[str | None] = mapped_column(db.String(255))
    access_mode: Mapped[ProjectAccess] = mapped_column(SAEnum(ProjectAccess), default=ProjectAccess.OPEN)
    start_date: Mapped[datetime | None] = mapped_column()
    end_date: Mapped[datetime | None] = mapped_column()
    submission_limit_per_user: Mapped[int | None] = mapped_column()
    manager_id: Mapped[int | None] = mapped_column(db.ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    manager: Mapped[User | None] = relationship("User", back_populates="managed_projects", foreign_keys=[manager_id])
    submissions: Mapped[list[Submission]] = relationship("Submission", back_populates="project", cascade="all,delete")

    __table_args__ = (
        CheckConstraint("rate_per_view_cents >= 0", name="ck_projects_rate_positive"),
        CheckConstraint("fixed_reward_cents >= 0", name="ck_projects_fixed_positive"),
    )

    def is_active(self) -> bool:
        now = datetime.utcnow()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def calculate_reward(self, views: int | None) -> int:
        views = views or 0
        if self.payment_type == PaymentType.PER_VIEW:
            rate = self.rate_per_view_cents or 0
            return views * rate
        return self.fixed_reward_cents or 0


class Submission(db.Model):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(db.ForeignKey("projects.id"), nullable=False)
    clipper_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    video_url: Mapped[str] = mapped_column(db.String(255), nullable=False)
    platform: Mapped[PlatformType] = mapped_column(SAEnum(PlatformType), nullable=False)
    views: Mapped[int | None] = mapped_column()
    status: Mapped[SubmissionStatus] = mapped_column(SAEnum(SubmissionStatus), default=SubmissionStatus.PENDING)
    reject_reason: Mapped[str | None] = mapped_column(db.String(200))
    reward_cents: Mapped[int | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    project: Mapped[Project] = relationship("Project", back_populates="submissions")
    clipper: Mapped[User] = relationship("User", back_populates="submissions", foreign_keys=[clipper_id])

    __table_args__ = (
        UniqueConstraint("project_id", "video_url", name="uq_submissions_project_video"),
    )


class PayoutRequest(db.Model):
    __tablename__ = "payout_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    amount_cents: Mapped[int] = mapped_column(nullable=False)
    method: Mapped[str] = mapped_column(db.String(50), nullable=False)
    details: Mapped[str] = mapped_column(db.String(255), nullable=False)
    status: Mapped[PayoutStatus] = mapped_column(SAEnum(PayoutStatus), default=PayoutStatus.PENDING)
    processed_by_id: Mapped[int | None] = mapped_column(db.ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship("User", foreign_keys=[user_id], back_populates="payout_requests")
    processed_by: Mapped[User | None] = relationship("User", foreign_keys=[processed_by_id])


class BalanceTransaction(db.Model):
    __tablename__ = "balance_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
    amount_cents: Mapped[int] = mapped_column(nullable=False)
    reason: Mapped[str] = mapped_column(db.String(255), nullable=False)
    tx_type: Mapped[BalanceType] = mapped_column(SAEnum(BalanceType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="balance_transactions")
