def serialTest(condition=True):
    """
    Decorator for running tests serially.  Requires pytest
    """
    def decorator(fn):
        if has_pytest and condition:
            return pytest.mark.serial(fn)
        return fn
    return decorator
