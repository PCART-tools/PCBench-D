def _apply_if_callable(maybe_callable, obj, **kwargs):
    """
    Evaluate possibly callable input using obj and kwargs if it is callable,
    otherwise return as it is
    """
    if callable(maybe_callable):
        return maybe_callable(obj, **kwargs)
    return maybe_callable
