@contextmanager
def use_skip_tracker(skip_tracker: SkipTracker) -> Generator[None, None, None]:
    """Registers the given skip tracker on the current thread within a
    context::

        with use_skip_tracker(my_skip_tracker):
            ...

    """
    orig = thread_local.skip_tracker

    thread_local.skip_tracker = skip_tracker

    try:
        yield
    finally:
        thread_local.skip_tracker = orig
