def display_name(fn: Callable) -> str:
    if hasattr(fn, "__qualname__"):
        return fn.__qualname__
    elif hasattr(fn, "__name__"):
        return fn.__name__
    else:
        return str(fn)
