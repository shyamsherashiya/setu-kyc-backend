from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.users import UserCreate

class CRUDUser:
    def create_user(self, db: Session, user_in: UserCreate):
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name
        )
        db_user.set_password(user_in.password)  
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

user_crud = CRUDUser()