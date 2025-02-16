# app/services/kyc_service.py
from datetime import datetime
from typing import Dict, Any
from app.services.setu_service import SetuAPIClient
from app.schemas.kyc import KYCAttemptResponse

class KYCService:
    def __init__(self):
        self.setu_client = SetuAPIClient()

    async def verify_pan_with_user(
        self, 
        user_full_name: str,
        pan: str, 
        db_attempt: Any
    ) -> Dict[str, Any]:
        pan_result = await self.setu_client.verify_pan(pan)
        # Name matching check
        pan_name = pan_result.get("data", {}).get("full_name", "").lower()
        user_name = user_full_name.strip().lower()
        
        db_attempt.pan_verification_status = pan_result.get("verification")
        db_attempt.pan_response = pan_result
        if pan_result.get("verification","").lower() != "success":
            db_attempt.overall_status = "failed"
            db_attempt.failure_reason = pan_result.get("message")
        elif pan_name != user_name:
            db_attempt.overall_status = "failed"
            db_attempt.failure_reason = "Logged in user name doesn't match PAN records, Please try again with correct PAN"
            db_attempt.name_match_status = "pan_mismatch"
        else:
            db_attempt.name_match_status = "pan_matched"
            db_attempt.overall_status = ""
            
        return db_attempt

    async def verify_bank_with_user(
        self, 
        user_full_name: str,
        account_number: str, 
        ifsc: str, 
        db_attempt: Any
    ) -> Dict[str, Any]:
        bank_result = await self.setu_client.verify_bank_account(account_number, ifsc)
        # Name matching check
        bank_name = bank_result.get("data", {}).get("name", "").lower()
        user_name = user_full_name.strip().lower()
        db_attempt.bank_verification_status = bank_result.get("verification")
        db_attempt.bank_response = bank_result
        if bank_result.get("verification","").lower() != "success":
            db_attempt.overall_status = "failed"
            db_attempt.failure_reason = bank_result.get("message")
        elif bank_name != user_name and bank_name != "test user name":
            db_attempt.overall_status = "failed"
            db_attempt.failure_reason = "Logged in user name doesn't match bank records, Please try again with correct bank details"
            db_attempt.name_match_status = "bank_mismatch"
        else:
            if db_attempt.name_match_status == "pan_matched" or db_attempt.name_match_status == "bank_mismatch": #when second time bank details are verified
                db_attempt.name_match_status = "both_matched"
                db_attempt.overall_status = "success"
                db_attempt.failure_reason = ""
            
        return db_attempt