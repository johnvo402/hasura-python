from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from .models import LoginData, LoginActionResponse
from ...utils.database import get_db
from ...utils.logger import get_logger
from ...models.account import Account
from ...config import settings
# from ...auth.context import current_account
from ...utils.result import Result


logger = get_logger(__name__)

async def handle_login_action(data: LoginData) -> Result[LoginActionResponse]:
    """Handle login action"""
    
    with next(get_db()) as db:
        # Query user from database with specific fields
        stmt = select(
            Account.id,
            Account.username,
            Account.password_hash,
            Account.is_active
        ).where(Account.username == data.username)
        user = db.execute(stmt).first()
        # Check if user exists and validate credentials
        if not user:
            return Result.fail(
                message="Invalid username or password",
                code=401,
                path="webhook.login_action",
                location="validate_credentials"
            )
        
        user_id, username, password_hash, is_active = user
        
        # Verify password (assuming verify_password is a static method in Account)
        if not Account.verify_password_hash(password_hash, data.password):
            return Result.fail(
                message="Invalid username or password",
                code=401,
                path="webhook.login_action",
                location="validate_credentials"
            )
        
        # Check if account is active
        if not is_active:
            logger.warning(f"Login attempt for disabled account: {username}")
            return Result.fail(
                message="Account is disabled",
                code=403,
                path="webhook.login_action",
                location="check_account_active"
            )
        
        # Update last login time
        db.query(Account).filter(Account.id == user_id).update(
            {"last_login": datetime.utcnow()}
        )
        db.commit()
        
        user_id = str(user_id)
        
    
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
    return Result.ok(
        data=LoginActionResponse(
            accessToken=access_token,
            refeshToken=refresh_token
        )
    )