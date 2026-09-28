from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CorrectionRequestCreate(BaseModel):
    parcel_id: Optional[str] = None
    title_id: Optional[str] = None
    correction_level: str  # clerical | technical | substantive
    description: str
    evidence_reference: Optional[str] = None


class CorrectionRequestRead(BaseModel):
    id: str
    parcel_id: Optional[str]
    title_id: Optional[str]
    correction_level: str
    description: str
    evidence_reference: Optional[str]
    status: str
    submitted_by: str
    reviewed_by: Optional[str]
    review_notes: Optional[str]
    submitted_at: datetime
    reviewed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class CorrectionReview(BaseModel):
    status: str  # approved | rejected | under_review
    review_notes: Optional[str] = None
