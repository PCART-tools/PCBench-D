def ops_wrapper(name: str) -> Callable[..., OpsValue]:
    assert isinstance(name, str)

    def fn(*args: object, **kwargs: object) -> OpsValue:
        return getattr(ops, name)(*args, **kwargs)

    return fn
