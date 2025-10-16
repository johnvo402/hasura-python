from typing import Dict
from webhook.auth.context import current_account

async def get_profile_handler() -> Dict:
    """Example action handler using current_account"""
    if not current_account.is_authenticated:
        raise Exception("Not authenticated")
    
    return {
        "profile": {
            "id": current_account.user_id,
            "email": current_account.email,
            "username": current_account.username,
            "role": current_account.role
        }
    }