def register_logger(logger: Logger) -> None:
    """Register custom logger.

    Parameters
    ----------
    logger : logging.Logger
        Custom logger.
    """
    if not isinstance(logger, Logger):
        raise TypeError("Logger should inherit logging.Logger class")
    global _LOGGER
    _LOGGER = logger
