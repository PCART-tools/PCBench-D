def custom_op(
    qualname: str, manual_schema: typing.Optional[str] = None
) -> typing.Callable:
    r"""
    This API is deprecated, please use torch.library.custom_op instead
    """
    warn_deprecated()

    def inner(func):
        if not inspect.isfunction(func):
            raise ValueError(
                f"custom_op(...)(func): Expected `func` to be a Python "
                f"function, got: {type(func)}"
            )

        ns, name = parse_qualname(qualname)
        validate_namespace(ns)
        if func.__name__ != name:
            raise ValueError(
                f"custom_op(qualname='{qualname}', ...)(func): expected `func` "
                f"to have name '{name}' but got '{func.__name__}'. "
                f"Please either change the name of `func` or the qualname that "
                f"is passed to `custom_op`"
            )

        schema = infer_schema(func, mutates_args=()) if manual_schema is None else manual_schema
        schema_str = f"{name}{schema}"
        function_schema = FunctionSchema.parse(schema_str)
        validate_schema(function_schema)
        if manual_schema is not None:
            validate_function_matches_schema(function_schema, func)

        lib = library.Library(ns, "FRAGMENT")
        lib.define(schema_str)
        ophandle = find_ophandle_or_throw(ns, function_schema.name)
        result = CustomOp(lib, ns, function_schema, name, ophandle, _private_access=True)

        result.__name__ = func.__name__
        result.__module__ = func.__module__
        result.__doc__ = func.__doc__

        library.impl(lib, result._opname, "Autograd")(
            autograd_kernel_indirection(weakref.proxy(result))
        )

        torch._C._dispatch_set_report_error_callback(
            ophandle, functools.partial(report_error_callback, weakref.proxy(result))
        )

        return result

    return inner
