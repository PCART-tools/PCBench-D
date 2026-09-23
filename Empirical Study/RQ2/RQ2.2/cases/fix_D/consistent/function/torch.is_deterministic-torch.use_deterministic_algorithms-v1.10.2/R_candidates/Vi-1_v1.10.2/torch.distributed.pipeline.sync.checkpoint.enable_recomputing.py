@contextmanager
def enable_recomputing() -> Generator[None, None, None]:
    """Makes :func:`is_recomputing` return :data:`True` within a context."""
    orig = thread_local.is_recomputing
    thread_local.is_recomputing = True
    try:
        yield
    finally:
        thread_local.is_recomputing = orig
