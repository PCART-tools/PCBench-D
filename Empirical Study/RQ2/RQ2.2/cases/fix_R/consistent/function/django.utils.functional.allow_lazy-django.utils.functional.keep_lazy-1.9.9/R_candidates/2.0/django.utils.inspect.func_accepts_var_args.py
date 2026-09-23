def func_accepts_var_args(func):
    """
    Return True if function 'func' accepts positional arguments *args.
    """
    return any(
        p for p in inspect.signature(func).parameters.values()
        if p.kind == p.VAR_POSITIONAL
    )
