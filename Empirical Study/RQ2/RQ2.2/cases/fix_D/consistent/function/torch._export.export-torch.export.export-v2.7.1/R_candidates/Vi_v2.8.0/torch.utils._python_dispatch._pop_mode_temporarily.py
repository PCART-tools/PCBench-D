@contextlib.contextmanager
def _pop_mode_temporarily(k: Optional[DispatchKey] = None):
    old = _pop_mode(k)
    try:
        yield old
    finally:
        _push_mode(old)
