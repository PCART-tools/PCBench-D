def normalize_range_iter(range_iter) -> tuple[int, int, int]:
    _, (range_obj,), maybe_idx = range_iter.__reduce__()
    # In 3.12+, `maybe_idx` could be None, and `range_obj.start` would've been
    # already incremented by the current index.
    start = range_obj.start + (maybe_idx or 0)
    stop = range_obj.stop
    step = range_obj.step
    return (start, stop, step)
