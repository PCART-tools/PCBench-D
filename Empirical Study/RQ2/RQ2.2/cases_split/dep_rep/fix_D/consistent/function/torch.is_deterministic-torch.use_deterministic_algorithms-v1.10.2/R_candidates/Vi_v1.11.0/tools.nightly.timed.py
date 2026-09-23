def timed(prefix: str) -> Callable[[F], F]:
    """Decorator for timing functions"""

    def dec(f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            global LOGGER
            logger = cast(logging.Logger, LOGGER)
            logger.info(prefix)
            with timer(logger, prefix):
                return f(*args, **kwargs)

        return cast(F, wrapper)

    return dec
