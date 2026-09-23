@contextlib.contextmanager
def EmptyDeviceScope():
    """
    Allow users to 'disable' the device scope behaviour (so it can be
    controlled at a NetDef::DeviceOption level, not overridden at
    OperatorDef::DeviceOption level).

    This sets the CurrentDeviceScope() to None, so that the field is
    not set in CreateOperator(...), etc.
    """
    old_scope = CurrentDeviceScope()
    try:
        _threadlocal_scope.devicescope = None
        yield
    finally:
        _threadlocal_scope.devicescope = old_scope
        return
