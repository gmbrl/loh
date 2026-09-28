import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _now():
    return datetime.now(timezone.utc)


class SurveyPlan(Base):
    """Technical survey document submitted by a licensed surveyor."""

    __tablename__ = "survey_plans"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    reference_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    # GeoJSON or WKT string for the boundary
    geometry: Mapped[str] = mapped_column(Text, nullable=True)
    area_sqm: Mapped[float] = mapped_column(Float, nullable=True)
    # Status: pending | approved | rejected
    status: Mapped[str] = mapped_column(
        Enum("pending", "approved", "rejected", name="survey_status"),
        default="pending",
        nullable=False,
    )
    submitted_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    reviewed_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    review_notes: Mapped[str] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    submitted_by_user = relationship("User", foreign_keys=[submitted_by], back_populates="survey_plans")
    reviewed_by_user = relationship("User", foreign_keys=[reviewed_by])
    parcel = relationship("Parcel", back_populates="survey_plan", uselist=False)


class Parcel(Base):
    """Official parcel activated by the cadastral authority after survey approval."""

    __tablename__ = "parcels"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    parcel_identifier: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    geometry: Mapped[str] = mapped_column(Text, nullable=True)
    area_sqm: Mapped[float] = mapped_column(Float, nullable=True)
    land_use: Mapped[str] = mapped_column(String(100), nullable=True)
    # Status: active | merged | cancelled
    status: Mapped[str] = mapped_column(
        Enum("active", "merged", "cancelled", name="parcel_status"),
        default="active",
        nullable=False,
    )
    survey_plan_id: Mapped[str] = mapped_column(
        ForeignKey("survey_plans.id"), nullable=False
    )
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    survey_plan = relationship("SurveyPlan", back_populates="parcel")
    created_by_user = relationship("User", foreign_keys=[created_by])
    titles = relationship("Title", back_populates="parcel")
    encumbrances = relationship("Encumbrance", back_populates="parcel")
    correction_requests = relationship("CorrectionRequest", back_populates="parcel")
