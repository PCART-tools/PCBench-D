def get_default_args(fn):
    if fn is None:
        return {}

    signature = inspect.signature(fn)

    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }
