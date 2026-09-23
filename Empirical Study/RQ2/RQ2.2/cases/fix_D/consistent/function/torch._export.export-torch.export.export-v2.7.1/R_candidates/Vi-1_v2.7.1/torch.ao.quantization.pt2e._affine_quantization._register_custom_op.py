def _register_custom_op(lib):
    """This decorator is used to preserve some high level operators for torch.export.export
    while still allow them to be decomposed for inductor path

    requirement: make sure `fn.__name__[1:]` is the operator name you want to register

    NOTE: This should be applied at the top, after all other decorators have been applied
    NOTE: We haven't tested the case when `fn` accepts tensor subclass instance as input,
    e.g. uint4 tensor subclass instance, and we'll probably need to figure out what would make
    sense for downstream system (like executorch) to accept as well

    Example:
        lib = torch.library.Library("my_namespace', "FRAGMENT")

        register_custom_op = _register_custom_op(lib)

        @register_custom_op
        def _the_op_that_needs_to_be_preserved(...)
            ...

        # after this, `_the_op_that_needs_to_be_preserved` will be preserved as
        # torch.ops.my_namespace.the_op_that_needs_to_be_preserved operator after
        # torch.export.export / torch._export.export_for_training

    """
    from torch._inductor.decomposition import register_decomposition

    def decorator(fn):
        from torch._library.infer_schema import infer_schema

        # expecting fn.__name__ starts with `_` and we want to take the rest
        # to be the name of the custom op
        assert (
            fn.__name__[0] == "_"
        ), f"Expecting function name starts with `_`, got {fn.__name__}"
        assert not any(
            c in fn.__name__ for c in ".<>"
        ), f"Expecting op to be defined in normal functions, not lambda or local: {fn.__name__}"
        op_name = fn.__name__[1:]
        schema = op_name + infer_schema(fn, mutates_args={})
        lib.define(schema)
        lib.impl(op_name, fn, "CompositeImplicitAutograd")

        lib_namespace = lib.ns
        op = getattr(getattr(torch.ops, lib_namespace), op_name)
        register_decomposition([op])(fn)
        return op

    return decorator
