def register_handler(handler):
    """
    Install application-specific HDF5 image handler.

    :param handler: Handler object.
    """
    global _handler
    _handler = handler
