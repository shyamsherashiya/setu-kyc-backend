# app/api/v1/endpoints/kyc.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.kyc_service import KYCService
from app.crud.crud_kyc import kyc_crud
from app.db.session import get_db
from app.schemas.kyc import PanVerificationRequest, BankVerificationRequest, KYCAttemptResponse
from app.core.security import get_current_user
from app.db.models import User


router = APIRouter(prefix="/kyc", tags=["kyc"])

@router.post("/initiate-pan", response_model=KYCAttemptResponse)
async def initiate_pan_verification(
    pan_data: PanVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create new attempt
    db_attempt = kyc_crud.create_kyc_attempt(db, current_user.id,pan_data=pan_data.dict())
    
    # Verify PAN and check name match
    kyc_service = KYCService()
    updated_attempt = await kyc_service.verify_pan_with_user(
        current_user.full_name,
        pan_data.pan_number,
        db_attempt
    )
    
    db.commit()
    return updated_attempt

@router.post("/initiate-bank", response_model=KYCAttemptResponse)
async def initiate_bank_verification(
    bank_data: BankVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get existing attempt
    db_attempt = kyc_crud.get_attempt(db, bank_data.attempt_id)
    
    # Validate attempt ownership
    if not db_attempt or db_attempt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="KYC attempt not found")
    
    # Check PAN verification status
    if db_attempt.failure_reason and db_attempt.failure_reason.lower() != "" and db_attempt.name_match_status and db_attempt.name_match_status.lower() == "pan_mismatch":
        raise HTTPException(status_code=400, detail="Complete PAN verification first")
    
    # Verify bank and check name match
    kyc_service = KYCService()
    updated_attempt = await kyc_service.verify_bank_with_user(
        current_user.full_name,
        bank_data.account_number,
        bank_data.ifsc_code,
        db_attempt
    )
    
    db.commit()
    return updated_attempt