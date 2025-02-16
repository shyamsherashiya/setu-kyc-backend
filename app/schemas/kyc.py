from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PanVerificationRequest(BaseModel):
    pan_number: str = Field(..., min_length=10, max_length=10, example="ABCDE1234A")

class BankVerificationRequest(BaseModel):
    attempt_id: int
    account_number: str = Field(..., min_length=9, max_length=18, example="1234567890")
    ifsc_code: str = Field(..., min_length=11, max_length=11, example="ABCD0123456")

class KYCAttemptResponse(BaseModel):
    id: int
    user_id: int
    pan_verification_status: Optional[str]
    bank_verification_status: Optional[str]
    name_match_status: Optional[str]
    overall_status: str
    failure_reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class KYCVerificationResponse(BaseModel):
    status: str
    message: str
    details: Optional[dict]
    timestamp: datetime