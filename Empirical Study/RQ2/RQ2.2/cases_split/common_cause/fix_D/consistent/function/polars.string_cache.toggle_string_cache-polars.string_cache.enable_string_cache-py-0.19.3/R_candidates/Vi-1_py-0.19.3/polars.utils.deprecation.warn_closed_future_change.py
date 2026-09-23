def warn_closed_future_change() -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Issue a warning to specify a value for `closed` as the default value will change.

    Decorator for rolling functions. Use as follows::

        @warn_closed_future_change()
        def rolling_min():
            ...

    """

    def decorate(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # we only warn if 'by' is passed in, otherwise 'closed' is not used
            if (kwargs.get("by") is not None) and ("closed" not in kwargs):
                issue_deprecation_warning(
                    "The default value for `closed` will change from 'left' to 'right' in a future version."
                    " Explicitly pass a value for `closed` to silence this warning.",
                    version="0.18.4",
                )
            return function(*args, **kwargs)

        return wrapper

    return decorate
