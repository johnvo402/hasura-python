from datetime import datetime, timedelta
import os
import jwt
from fastapi import Request
from .context import current_account

        # Fetch user data from database
from ..models.account import Account
from ..utils.database import SessionLocal

async def verify_token_handler(request: Request):
    """Handle Hasura auth webhook verification"""
    try:
        # Try to get token from different possible locations
        auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
        
        # If not in headers, check the request body
        if not auth_header:
            body = await request.json()
            
            # Check if token is in the nested headers structure
            if isinstance(body, dict) and 'headers' in body:
                body_headers = body['headers']
                auth_header = body_headers.get('authorization') or body_headers.get('Authorization')
            
        if not auth_header:
            current_account.clear_context()
            return {
                "x-hasura-role": "anonymous",
            }
        
        # Extract the token (Remove 'Bearer ' from the header)
        token = auth_header.replace('Bearer ', '')
        
        # Verify and decode the JWT token using the same secret as login
        from ..config import settings
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        
        # Extract user_id from the token (stored in 'sub' claim)
        user_id = str(payload.get('sub'))
        if not user_id:
            return {"message": "User ID not found in token"}


        db = SessionLocal()
        try:
            account = db.query(Account).filter(Account.id == user_id).first()
            if not account:
                return {"message": "User not found in database"}

            account_data = {
                'user_id': str(account.id),
                'email': account.email,
                'username': account.username,
                'role': account.role
            }
            
            current_account.init_context(account_data)
            return {
                "x-hasura-role": account_data['role'],
                "x-hasura-user-id": account_data['user_id'],
                "x-hasura-email": account_data['email'],
                "x-hasura-username": account_data['username'],
            }
        finally:
            db.close()
    except jwt.ExpiredSignatureError:
        current_account.clear_context()
        return {
            "x-hasura-role": "anonymous",
        }
    except jwt.InvalidTokenError:
        current_account.clear_context()
        return {
            "x-hasura-role": "anonymous",
        }
    except Exception as e:
        current_account.clear_context()
        return {
            "x-hasura-role": "anonymous",
        }