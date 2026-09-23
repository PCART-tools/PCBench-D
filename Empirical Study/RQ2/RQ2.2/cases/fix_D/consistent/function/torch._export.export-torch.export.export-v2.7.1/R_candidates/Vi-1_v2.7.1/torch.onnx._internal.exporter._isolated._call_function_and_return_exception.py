def _call_function_and_return_exception(func, args, kwargs):
    """Call function and return a exception if there is one."""

    try:
        return func(*args, **kwargs)
    except Exception as e:
        return e
