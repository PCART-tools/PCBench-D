def range_push(msg):
    """
    Pushes a range onto a stack of nested range span.  Returns zero-based
    depth of the range that is started.

    Args:
        msg (string): ASCII message to associate with range
    """
    return _nvtx.rangePushA(msg)
