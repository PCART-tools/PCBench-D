def wrap_method(method):
    """
    Wrap a method as a module so that it can be exported.
    The wrapped module's forward points to the method, and
    the method's original module state is shared.
    """
    assert ismethod(
        method,
    ), f"Expected {method} to be a method"
    return _WrappedMethod(method)
