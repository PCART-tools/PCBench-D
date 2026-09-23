@functools.lru_cache(None)
def _step_logger() -> Callable[..., None]:
    return dynamo_logging.get_step_logger(log)
