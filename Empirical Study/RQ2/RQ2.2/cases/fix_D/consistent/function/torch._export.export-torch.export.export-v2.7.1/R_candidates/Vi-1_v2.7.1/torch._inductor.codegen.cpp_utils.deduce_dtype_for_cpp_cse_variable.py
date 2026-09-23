def deduce_dtype_for_cpp_cse_variable(name, *args, **kwargs):
    if (
        output_dtype := deduce_output_dtype_by_name(
            name,
            *args,
            **kwargs,
        )
    ) is not None:
        return output_dtype
    elif name == "masked":
        # <TODO> Leslie: perhaps we can also deduce the masked dtype by
        # inputs' CppCseVariable like other. Let's check it if any
        # unexpected failures.
        assert (
            hasattr(V.interpreter, "current_node")
            and V.interpreter.current_node.target.startswith("masked_subblock")
            and get_current_node_opt_ctx() is not None
        )
        return get_current_node_opt_ctx().dtype
    else:
        # deduce output dtype by inputs' dtype
        assert all(
            arg.dtype is not None for arg in args if isinstance(arg, CppCSEVariable)
        )
        return functools.reduce(
            torch.promote_types,  # type: ignore[arg-type]
            [arg.dtype for arg in args if isinstance(arg, CppCSEVariable)],
        )
