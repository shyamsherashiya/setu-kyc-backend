from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.users import UserCreate, UserResponse
from app.crud.crud_user import user_crud
from app.db.session import get_db
from app.core.security import create_access_token

router = APIRouter(tags=["auth"])

# @router.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     if user_crud.get_user_by_email(db, user.email):
#         raise HTTPException(400, "Email already registered")
    
#     # Hash password before saving
#     hashed_password = pwd_context.hash(user.password)
#     db_user = user_crud.create_user(db, {
#         "email": user.email,
#         "full_name": user.full_name,
#         "password": hashed_password
#     })
#     return {"message": "User created successfully"}

# @router.post("/login")
# def login(credentials: UserLogin, db: Session = Depends(get_db)):
#     user = user_crud.get_user_by_email(db, credentials.email)
#     if not user or not user.verify_password(credentials.password):
#         raise HTTPException(401, "Invalid credentials")
#     return {"message": "Login successful"}


# @router.post("/register", response_model=UserResponse)
# def register(user: UserCreate, db = Depends(get_db)):
#     db_user = user_crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return user_crud.create_user(db, user)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return {
        "access_token": create_access_token({"sub": user.email}),
        "token_type": "bearer",
    }