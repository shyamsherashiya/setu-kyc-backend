from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserResponse
from app.crud.crud_user import user_crud
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user)

# @router.get("/{user_id}", response_model=UserResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user