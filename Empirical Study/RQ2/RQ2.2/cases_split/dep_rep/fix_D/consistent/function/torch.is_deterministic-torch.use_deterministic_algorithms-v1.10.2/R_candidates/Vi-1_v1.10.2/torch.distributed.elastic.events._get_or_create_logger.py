def _get_or_create_logger(destination: str = "null") -> logging.Logger:
    """
    Constructs python logger based on the destination type or extends if provided.
    Available destination could be found in ``handlers.py`` file.
    The constructed logger does not propagate messages to the upper level loggers,
    e.g. root logger. This makes sure that a single event can be processed once.

    Args:
        destination: The string representation of the event handler.
            Available handlers found in ``handlers`` module
    """
    global _events_loggers

    if destination not in _events_loggers:
        _events_logger = logging.getLogger(f"torchelastic-events-{destination}")
        _events_logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
        # Do not propagate message to the root logger
        _events_logger.propagate = False

        logging_handler = get_logging_handler(destination)
        _events_logger.addHandler(logging_handler)

        # Add the logger to the global dictionary
        _events_loggers[destination] = _events_logger

    return _events_loggers[destination]
