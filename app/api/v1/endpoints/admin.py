from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.admin import AnalyticsResponse, UserKYCHistory
from app.crud.crud_kyc import kyc_crud
from app.db.session import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    attempts = kyc_crud.get_all_attempts(db)
    
    return {
        "total_attempts": len(attempts),
        "successful_kyc": sum(1 for a in attempts if a.overall_status == "success"),
        "failed_kyc": sum(1 for a in attempts if a.overall_status == "failed"),
        "pan_failures": sum(1 for a in attempts if a.pan_verification_status == "failed"),
        "bank_failures": sum(1 for a in attempts if a.bank_verification_status == "failed"),
        "both_failures": sum(1 for a in attempts if 
                            a.pan_verification_status == "failed" and 
                            a.bank_verification_status == "failed"),
        "last_updated": datetime.now()
    }

@router.get("/user-history/{user_id}", response_model=UserKYCHistory)
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    attempts = kyc_crud.get_user_attempts(db, user_id)
    if not attempts:
        raise HTTPException(status_code=404, detail="No KYC attempts found")
    
    return {
        "user_id": user_id,
        "attempts": [a.__dict__ for a in attempts],
        "first_attempt": min(a.created_at for a in attempts),
        "last_attempt": max(a.created_at for a in attempts)
    }