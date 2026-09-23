def deprecate_renamed_parameter(
    old_name: str, new_name: str, *, version: str
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to mark a function argument as deprecated due to being renamed.

    Use as follows::

        @deprecate_renamed_parameter("old_name", "new_name", version="0.1.2")
        def myfunc(new_name):
            ...

    """

    def decorate(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            _rename_keyword_argument(
                old_name, new_name, kwargs, function.__name__, version
            )
            return function(*args, **kwargs)

        return wrapper

    return decorate
