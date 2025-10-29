
from .create_account import EVENT_NAME, EVENT_HANDLE
# Event handler mapping
# Each action module should expose EVENT_NAME, INPUT_MODEL, and HANDLER
event_handlers = {
    EVENT_NAME: EVENT_HANDLE
    # LOGIN_EVENT: (LOGIN_MODEL, LOGIN_HANDLER),
    # Add more mappings here as:
    # MODULE.EVENT_NAME: (MODULE.INPUT_MODEL, MODULE.HANDLER),
}