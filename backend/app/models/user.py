import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.permissions import Role
from app.database import Base


def _now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum(*[r.value for r in Role], name="user_role"),
        nullable=False,
        default=Role.CITIZEN.value,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now
    )

    # relationships
    survey_plans = relationship("SurveyPlan", back_populates="submitted_by_user")
    title_applications = relationship("TitleApplication", back_populates="submitted_by_user")
    encumbrance_submissions = relationship("Encumbrance", back_populates="submitted_by_user")
    correction_requests = relationship("CorrectionRequest", back_populates="submitted_by_user")

    def __repr__(self) -> str:
        return f"<User {self.email} [{self.role}]>"
