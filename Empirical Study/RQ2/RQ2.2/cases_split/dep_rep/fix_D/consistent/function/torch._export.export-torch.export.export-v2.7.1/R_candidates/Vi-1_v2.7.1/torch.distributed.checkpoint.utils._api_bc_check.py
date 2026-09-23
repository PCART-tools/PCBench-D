def _api_bc_check(func):
    @wraps(func)
    def inner_func(*args, **kwargs) -> Any:
        if len(args) == 2:
            warnings.warn(
                f"The argument order of {func.__name__} has been changed. "
                "Please check the document to avoid future breakages."
            )
            sig = inspect.signature(func)
            kwonlyargs = [
                p.name for p in sig.parameters.values() if p.kind == p.KEYWORD_ONLY
            ]
            if "storage_writer" in kwonlyargs:
                assert "storage_writer" not in kwargs, (args, kwargs)
                kwargs["storage_writer"] = args[1]
            elif "storage_reader" in kwonlyargs:
                assert "storage_reader" not in kwargs, (args, kwargs)
                kwargs["storage_reader"] = args[1]
            else:
                raise RuntimeError(f"Unexpected kwonlyargs = {kwonlyargs}")
            return func(args[0], **kwargs)
        else:
            return func(*args, **kwargs)

    return inner_func
