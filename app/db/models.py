from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .session import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class KYCAttempt(Base):
    __tablename__ = "kyc_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # PAN Verification Details
    pan_number = Column(String)
    pan_verification_status = Column(String)
    pan_details = Column(JSON)
    
    # Bank Verification Details
    account_number = Column(String)
    ifsc = Column(String)
    bank_verification_status = Column(String)
    bank_details = Column(JSON)
    
    # Metadata
    name_match_status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    overall_status = Column(String)
    failure_reason = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="kyc_attempts")

# Association table for many-to-many user-group relationship
user_group_association = Table(
    'user_group_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('user_groups.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    groups = relationship("UserGroup", secondary=user_group_association, back_populates="users")

    kyc_attempts = relationship("KYCAttempt", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.password_hash)


class UserGroup(Base):
    __tablename__ = "user_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # e.g., "admin", "user"
    
    users = relationship("User", secondary=user_group_association, back_populates="groups")

