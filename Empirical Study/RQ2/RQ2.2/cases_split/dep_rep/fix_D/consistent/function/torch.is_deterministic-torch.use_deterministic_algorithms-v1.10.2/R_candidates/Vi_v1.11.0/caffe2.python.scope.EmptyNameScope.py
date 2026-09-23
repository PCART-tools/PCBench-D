@contextlib.contextmanager
def EmptyNameScope():
    """
    Allow users to 'disable' the name scope behaviour.

    This sets the CurrentNameScope() to None, so that the field is
    not set in CreateOperator(...), etc.
    """
    old_scope = CurrentNameScope()
    try:
        _threadlocal_scope.namescope = ''
        yield
    finally:
        _threadlocal_scope.namescope = old_scope
        return
