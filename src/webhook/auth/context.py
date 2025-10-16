from typing import Optional, Dict
from fastapi import Request

class CurrentAccount:
    _instance = None
    _context = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentAccount, cls).__new__(cls)
        return cls._instance

    @classmethod
    def init_context(cls, account_data: Dict):
        """Initialize the context with account data"""
        cls._context = account_data

    @classmethod
    def clear_context(cls):
        """Clear the current context"""
        cls._context = {}

    @property
    def user_id(self) -> Optional[str]:
        return self._context.get('user_id')

    @property
    def email(self) -> Optional[str]:
        return self._context.get('email')

    @property
    def username(self) -> Optional[str]:
        return self._context.get('username')

    @property
    def role(self) -> str:
        return self._context.get('role', 'any')

    @property
    def is_authenticated(self) -> bool:
        return bool(self._context.get('user_id'))

current_account = CurrentAccount()