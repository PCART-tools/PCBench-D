@contextlib.contextmanager
def timer(logger: logging.Logger, prefix: str) -> Iterator[None]:
    """Timed context manager"""
    start_time = time.time()
    yield
    logger.info(f"{prefix} took {time.time() - start_time:.3f} [s]")
