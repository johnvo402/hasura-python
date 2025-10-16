from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import LoginData, LoginActionResponse
from ...utils.database import get_db
from ...utils.logger import get_logger
from ...models.account import Account
from ...config import settings

logger = get_logger(__name__)

async def handle_login_action(data: LoginData) -> LoginActionResponse:
    """Handle login action"""
    logger.info(f"Login attempt for user: {data.username}")
    
    with next(get_db()) as db:
        # Query user from database
        user = db.query(Account).filter(Account.username == data.username).first()
        print("User fetched from DB:", user.password_hash if user else "No user found")
        # Check if user exists and validate password
        if not user or not user.verify_password(data.password):
            logger.warning(f"Failed login attempt for user: {data.username}")
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        # Check if account is active
        if not user.is_active:
            logger.warning(f"Login attempt for disabled account: {data.username}")
            raise HTTPException(
                status_code=403,
                detail="Account is disabled"
            )
        
        # Update last login time
        user.update_last_login()
        db.commit()
        
        user_id = str(user.id)
        roles = [user.role]
        logger.info(f"Successful login for user: {data.username} with role: {user.role}")
    
    
    # Generate access token
    access_claims = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS),
    }
    access_token = jwt.encode(access_claims, settings.JWT_SECRET_KEY, algorithm="HS256")
    
    refresh_claims = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "type": "refresh"
    }
    refresh_token = jwt.encode(refresh_claims, settings.JWT_SECRET_KEY, algorithm="HS256")
    
    return LoginActionResponse(
        accessToken=access_token,
        refeshToken=refresh_token
    )