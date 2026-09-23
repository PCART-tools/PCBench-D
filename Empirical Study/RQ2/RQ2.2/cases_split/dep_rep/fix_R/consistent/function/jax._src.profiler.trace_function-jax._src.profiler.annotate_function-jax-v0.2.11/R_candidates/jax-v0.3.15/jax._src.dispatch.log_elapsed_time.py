@contextlib.contextmanager
def log_elapsed_time(fmt: str):
  if _on_exit:
    yield
  else:
    log_priority = logging.WARNING if config.jax_log_compiles else logging.DEBUG
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    logging.log(log_priority, fmt.format(elapsed_time=elapsed_time))
