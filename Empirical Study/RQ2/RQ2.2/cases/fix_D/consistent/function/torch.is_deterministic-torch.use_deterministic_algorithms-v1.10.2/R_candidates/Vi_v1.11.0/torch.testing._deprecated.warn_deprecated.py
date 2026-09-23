def warn_deprecated(instructions: Union[str, Callable[[str, Tuple[Any, ...], Dict[str, Any], Any], str]]) -> Callable:
    def outer_wrapper(fn: Callable) -> Callable:
        name = fn.__name__
        head = f"torch.testing.{name}() is deprecated and will be removed in a future release. "

        @functools.wraps(fn)
        def inner_wrapper(*args: Any, **kwargs: Any) -> Any:
            return_value = fn(*args, **kwargs)
            tail = instructions(name, args, kwargs, return_value) if callable(instructions) else instructions
            msg = (head + tail).strip()
            warnings.warn(msg, FutureWarning)
            return return_value

        return inner_wrapper

    return outer_wrapper
