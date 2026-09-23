def init():
    """
    Explicitly initializes the Python Imaging Library. This function
    loads all available file format drivers.
    """

    global _initialized
    if _initialized >= 2:
        return 0

    for plugin in _plugins:
        try:
            logger.debug("Importing %s", plugin)
            __import__(f"PIL.{plugin}", globals(), locals(), [])
        except ImportError as e:
            logger.debug("Image: failed to import %s: %s", plugin, e)

    if OPEN or SAVE:
        _initialized = 2
        return 1
