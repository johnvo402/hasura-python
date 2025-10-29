

from ...utils.database import get_db
from ...utils.logger import get_logger
# from ...auth.context import current_account
from ...utils.result import Result
from ...pkgs import SessionVariable
from ..models import ScheduleModel


logger = get_logger(__name__)

async def handle_test_cron(payload: ScheduleModel) -> Result[str]:
    """Handle login action"""
    print("payload", payload.payload, payload.name)
    return Result.ok(data="success")