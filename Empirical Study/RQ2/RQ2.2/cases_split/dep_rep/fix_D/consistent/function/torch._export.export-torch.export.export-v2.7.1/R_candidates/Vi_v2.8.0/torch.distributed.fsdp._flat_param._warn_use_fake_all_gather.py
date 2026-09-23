@functools.lru_cache(1)
def _warn_use_fake_all_gather(log: logging.Logger, warning: str):
    logger.warning(warning)
