from .models import LoginData, LoginActionResponse
from .handler import handle_login_action

# Action registration
ACTION_NAME = "login"
INPUT_MODEL = LoginData
HANDLER = handle_login_action