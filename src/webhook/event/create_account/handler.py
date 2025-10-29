from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from ...utils.database import get_db
from ...utils.logger import get_logger
from ...models.account import Account
from ...config import settings
# from ...auth.context import current_account
from ...utils.result import Result
from ...pkgs import SessionVariable
from ..models import EventContent


logger = get_logger(__name__)

async def handle_create_account_event(event: EventContent) -> Result[str]:
    """Handle login action"""
    print("payload", event.data.new)
    return Result.ok(data="success")