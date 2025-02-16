from pydantic import BaseModel
from datetime import datetime

class AnalyticsResponse(BaseModel):
    total_attempts: int
    successful_kyc: int
    failed_kyc: int
    pan_failures: int
    bank_failures: int
    both_failures: int
    last_updated: datetime

class UserKYCHistory(BaseModel):
    user_id: int
    attempts: list[dict]
    first_attempt: datetime
    last_attempt: datetime