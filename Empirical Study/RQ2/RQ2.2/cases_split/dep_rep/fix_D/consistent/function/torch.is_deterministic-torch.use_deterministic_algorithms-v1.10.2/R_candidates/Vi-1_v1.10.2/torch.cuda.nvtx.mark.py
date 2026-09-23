def mark(msg):
    """
    Describe an instantaneous event that occurred at some point.

    Args:
        msg (string): ASCII message to associate with the event.
    """
    return _nvtx.markA(msg)
