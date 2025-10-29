
from .test_cron import *
# Event handler mapping
# Each action module should expose EVENT_NAME, INPUT_MODEL, and HANDLER
schedule_handlers = {
    SCHEDULE_NAME: SCHEDULE_HANDLE
    # LOGIN_EVENT: (LOGIN_MODEL, LOGIN_HANDLER),
    # Add more mappings here as:
    # MODULE.EVENT_NAME: (MODULE.INPUT_MODEL, MODULE.HANDLER),
}