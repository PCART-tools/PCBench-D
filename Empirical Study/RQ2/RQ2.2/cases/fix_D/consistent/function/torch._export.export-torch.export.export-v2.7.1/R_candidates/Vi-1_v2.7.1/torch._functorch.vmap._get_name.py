def _get_name(func: Callable):
    if hasattr(func, "__name__"):
        return func.__name__

    if isinstance(func, functools.partial):
        return f"functools.partial({_get_name(func.func)}, ...)"

    # Not all callables have __name__, in fact, only static functions/methods
    # do.  A callable created via nn.Module, to name one example, doesn't have a
    # __name__.
    return repr(func)
