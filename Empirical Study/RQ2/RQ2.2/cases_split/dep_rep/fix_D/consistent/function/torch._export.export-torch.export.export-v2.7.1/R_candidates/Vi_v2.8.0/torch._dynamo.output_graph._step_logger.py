@functools.cache
def _step_logger():
    return torchdynamo_logging.get_step_logger(log)
