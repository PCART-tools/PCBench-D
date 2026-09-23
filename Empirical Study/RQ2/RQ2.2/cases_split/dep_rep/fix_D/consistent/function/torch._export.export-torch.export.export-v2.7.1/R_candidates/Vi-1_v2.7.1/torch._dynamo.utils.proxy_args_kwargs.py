def proxy_args_kwargs(args, kwargs):
    try:
        proxy_args = tuple(arg.as_proxy() for arg in args)
        proxy_kwargs = {key: arg.as_proxy() for key, arg in kwargs.items()}
        return proxy_args, proxy_kwargs
    except NotImplementedError as e:
        from .exc import unimplemented_v2
        from .variables.base import typestr

        unimplemented_v2(
            gb_type="Failed to convert args/kwargs to proxy",
            context=f"call_function args: {typestr(*args)} {typestr(*list(kwargs.values()))}",
            explanation="Missing `as_proxy()` implementation for some arg/kwarg.",
            hints=[],
            from_exc=e,
        )
