def SetErrorHandler(handler):
    """Registers an error handler for errors from registering operators

    Since the lazy registration may happen at a much later time, having a dedicated
    error handler allows for custom error handling logic. It is highly
    recomended to set this to prevent errors from bubbling up in weird parts of the
    code.

    Args:
        handler: a function that takes an exception as a single handler.
    Returns:
        None
    """

    global _error_handler
    _error_handler = handler
