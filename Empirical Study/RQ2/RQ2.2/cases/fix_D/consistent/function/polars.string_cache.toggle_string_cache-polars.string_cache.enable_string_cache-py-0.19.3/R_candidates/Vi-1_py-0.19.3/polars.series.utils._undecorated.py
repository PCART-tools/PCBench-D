def _undecorated(function: Callable[P, T]) -> Callable[P, T]:
    """Return the given function without any decorators."""
    while hasattr(function, "__wrapped__"):
        function = function.__wrapped__
    return function
