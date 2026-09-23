def register_handler(handler):
    """
    Install application-specific BUFR image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler
