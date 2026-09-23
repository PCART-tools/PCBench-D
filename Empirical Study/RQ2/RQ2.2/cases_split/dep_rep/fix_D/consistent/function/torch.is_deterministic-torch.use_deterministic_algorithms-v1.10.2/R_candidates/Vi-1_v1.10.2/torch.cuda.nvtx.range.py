@contextmanager
def range(msg, *args, **kwargs):
    """
    Context manager / decorator that pushes an NVTX range at the beginning
    of its scope, and pops it at the end. If extra arguments are given,
    they are passed as arguments to msg.format().

    Args:
        msg (string): message to associate with the range
    """
    range_push(msg.format(*args, **kwargs))
    yield
    range_pop()
