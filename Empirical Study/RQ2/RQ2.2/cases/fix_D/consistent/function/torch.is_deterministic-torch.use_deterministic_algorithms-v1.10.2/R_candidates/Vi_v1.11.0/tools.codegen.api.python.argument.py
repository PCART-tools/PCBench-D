def argument(a: Argument) -> PythonArgument:
    return PythonArgument(
        name=a.name,
        type=a.type,
        # TODO: directly translate a.default to python default
        default=str(pythonify_default(cpp.default_expr(a.default, a.type)))
        if a.default is not None else None,
        default_init=None,
    )
