def current_skip_tracker() -> SkipTracker:
    """Gets the skip tracker on the current thread."""
    skip_tracker = thread_local.skip_tracker

    if skip_tracker is None:
        skip_tracker = SkipTracker()
        thread_local.skip_tracker = skip_tracker

    return skip_tracker
