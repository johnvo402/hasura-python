from .login_action import ACTION_NAME as LOGIN_ACTION, HANDLER as LOGIN_HANDLER

# Action handler mapping
# Each action module should expose ACTION_NAME, INPUT_MODEL, and HANDLER
action_handlers = {
    LOGIN_ACTION: LOGIN_HANDLER,
    # Add more mappings here as:
    # MODULE.ACTION_NAME: (MODULE.INPUT_MODEL, MODULE.HANDLER),
}