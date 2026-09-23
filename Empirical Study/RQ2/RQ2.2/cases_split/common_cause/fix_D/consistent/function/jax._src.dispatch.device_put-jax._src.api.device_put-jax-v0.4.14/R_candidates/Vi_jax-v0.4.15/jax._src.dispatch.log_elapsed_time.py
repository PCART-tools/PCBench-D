@contextlib.contextmanager
def log_elapsed_time(fmt: str, fun_name: str, event: str | None = None):
  if _on_exit:
    yield
  else:
    log_priority = logging.WARNING if config.jax_log_compiles else logging.DEBUG
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    if logger.isEnabledFor(log_priority):
      logger.log(log_priority, fmt.format(
          fun_name=fun_name, elapsed_time=elapsed_time))
    if event is not None:
      record_event_duration_secs(event, elapsed_time)
