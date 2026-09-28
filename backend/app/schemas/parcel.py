from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SurveyPlanCreate(BaseModel):
    reference_number: str
    description: Optional[str] = None
    geometry: Optional[str] = None
    area_sqm: Optional[float] = None


class SurveyPlanRead(BaseModel):
    id: str
    reference_number: str
    description: Optional[str]
    geometry: Optional[str]
    area_sqm: Optional[float]
    status: str
    submitted_by: str
    reviewed_by: Optional[str]
    review_notes: Optional[str]
    submitted_at: datetime
    reviewed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class SurveyPlanReview(BaseModel):
    status: str  # "approved" | "rejected"
    review_notes: Optional[str] = None


class ParcelCreate(BaseModel):
    """Created by cadastral officer after survey approval."""
    parcel_identifier: str
    survey_plan_id: str
    description: Optional[str] = None
    geometry: Optional[str] = None
    area_sqm: Optional[float] = None
    land_use: Optional[str] = None


class ParcelRead(BaseModel):
    id: str
    parcel_identifier: str
    description: Optional[str]
    geometry: Optional[str]
    area_sqm: Optional[float]
    land_use: Optional[str]
    status: str
    survey_plan_id: str
    created_by: str
    created_at: datetime

    model_config = {"from_attributes": True}
