from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from sqlalchemy.sql import func
import bcrypt
from ..utils.database import Base

class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default='any')
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    def set_password(self, plain_password: str):
        """Hash and set the password"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        self.password_hash = hashed.decode('utf-8')

    def verify_password(self, plain_password: str) -> bool:
        """Verify the password"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login_at = func.now()