def registered_extensions():
    """
    Returns a dictionary containing all file extensions belonging
    to registered plugins
    """
    if not EXTENSION:
        init()
    return EXTENSION
