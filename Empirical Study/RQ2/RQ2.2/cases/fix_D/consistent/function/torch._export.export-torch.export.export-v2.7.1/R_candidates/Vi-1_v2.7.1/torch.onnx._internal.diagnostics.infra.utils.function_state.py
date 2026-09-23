def function_state(
    fn: Callable, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> Mapping[str, Any]:
    bind = inspect.signature(fn).bind(*args, **kwargs)
    return bind.arguments
