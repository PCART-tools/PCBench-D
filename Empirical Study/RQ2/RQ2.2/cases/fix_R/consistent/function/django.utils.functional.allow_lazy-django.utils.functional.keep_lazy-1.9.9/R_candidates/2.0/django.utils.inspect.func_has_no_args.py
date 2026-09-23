def func_has_no_args(func):
    args = [
        p for p in inspect.signature(func).parameters.values()
        if p.kind == p.POSITIONAL_OR_KEYWORD
    ]
    return len(args) == 1
