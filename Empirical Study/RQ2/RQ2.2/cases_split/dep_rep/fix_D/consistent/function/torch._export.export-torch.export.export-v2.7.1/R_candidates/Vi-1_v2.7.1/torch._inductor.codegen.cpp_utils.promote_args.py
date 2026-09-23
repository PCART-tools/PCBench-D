def promote_args(new_args):
    def promote_arg(arg, promote_type):
        if (
            isinstance(arg, CppCSEVariable)
            and arg.dtype
            and promote_type
            and arg.dtype != promote_type
        ):
            arg = ops.to_dtype(arg, promote_type)
            arg = arg.value if isinstance(arg, OpsValue) else arg
            arg.dtype = promote_type
        return arg

    promote_type = get_promote_dtype(new_args)
    promote_fn = functools.partial(
        promote_arg,
        promote_type=promote_type,
    )
    if (
        all(
            new_arg.dtype is not None
            for new_arg in new_args
            if isinstance(new_arg, CppCSEVariable)
        )
        and promote_type
    ):
        new_args = list(map(promote_fn, new_args))
    return new_args
