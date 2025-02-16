from fastapi import FastAPI
from app.api.v1.endpoints import users, kyc, admin,auth
from app.db.session import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(kyc.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/")
def health_check():
    return {"status": "ok"}