from sqlalchemy.orm import Session
from app.db.models import KYCAttempt

class CRUDKYC:
    def create_kyc_attempt(self, db: Session, user_id: int, pan_data: dict):
        db_attempt = KYCAttempt(user_id=user_id, **pan_data)
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
        return db_attempt

    def update_bank_details(self, db: Session, attempt_id: int, bank_data: dict):
        attempt = db.query(KYCAttempt).filter(KYCAttempt.id == attempt_id).first()
        if not attempt:
            return None
        for key, value in bank_data.items():
            setattr(attempt, key, value)
        db.commit()
        db.refresh(attempt)
        return attempt

    def get_attempt(self, db: Session, attempt_id: int):
        return db.query(KYCAttempt).filter(KYCAttempt.id == attempt_id).first()

    def get_user_attempts(self, db: Session, user_id: int):
        return db.query(KYCAttempt).filter(KYCAttempt.user_id == user_id).all()

kyc_crud = CRUDKYC()