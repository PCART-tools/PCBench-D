@functools.lru_cache(1)
def _warn_skip_writeback_check(log: logging.Logger, warning: str):
    logger.warning(warning)
