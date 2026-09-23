@functools.lru_cache(1)
def _warn_use_fake_reduce(log: logging.Logger, warning: str):
    logger.warning(warning)
