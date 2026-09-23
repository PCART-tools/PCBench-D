def _correct_storage_aliasing(func, schema_info, args, outs):
    """
    Given: an OpOverload, a SchemaInfo (cached information from torchgen about schema),
    and the inputs/outputs to the OpOverload,
    this function checks to see if func is a view operator
    (by checking if any of the outputs in the op's schema
     are immutable aliases of inputs).
    If so, this function manually aliases the storage of the output tensor
    with its corresponding input tensor alias.
    It does this by unsafely overwriting the storage field of the output tensor
    to be the same storage as the input.
    """
    assert isinstance(func, torch._ops.OpOverload)
    assert isinstance(args, tuple)
    assert isinstance(outs, (list, tuple))

    def alias_non_inplace_storage(arg, ret):
        # This is hopefully a reasonable assert:
        # subclasses that rely on this API for output aliasing
        # should always return wrapper tensor subclasses for us to manually alias.
        # in theory if a subclass that needs this API wants to sometimes return
        # plain tensors, we could remove the assert and just not perform the aliasing,
        # but it seems safer to learn more about this case first.
        if is_traceable_wrapper_subclass(arg) or is_traceable_wrapper_subclass(ret):
            ret_list = ret if isinstance(ret, list) else [ret]
            for r in ret_list:
                assert type(arg) == type(
                    r
                ), f"""Called {str(func)} with input of type {type(arg)}
and output of type {type(ret)}. But expected types to match."""
        # Need to call a non-dispatcher helper, because we explicitly do **not**
        # want our subclass to intercept the set_() call.
        # instead, our subclass should directly have its storage swapped out.
        # we **explicitly** don't want to reset the sizes on ret, if the storage implies a size change.
        # Why?
        # The purpose of this API is *not* to change the size/strides of our output- we assume it's already correct.
        # We just want to "fix up" the storage aliasing, without modifying or output's metadata.
        # Example: out = inp.expand(inp.shape[0], inp.shape[0])
        #     This requires swapping the storage of out to be the same as inp,
        #     but we do *not* want it to change the sizes/strides that were compute for out.

        if isinstance(ret, list):
            for r in ret:
                torch._functionalize_unsafe_set(r, arg)
        else:
            assert isinstance(ret, torch.Tensor), f"type: {type(ret)}"
            torch._functionalize_unsafe_set(ret, arg)

    def is_read_only_alias_match(arg, ret):
        shared_aliases = arg.alias_set & ret.alias_set
        return len(shared_aliases) > 0 and not arg.is_write

    num_args = len(func._schema.arguments)
    num_returns = len(func._schema.returns)
    for arg_idx in range(num_args):
        for return_idx in range(num_returns):
            if is_read_only_alias_match(
                schema_info.args[arg_idx], schema_info.outs[return_idx]
            ):
                alias_non_inplace_storage(args[arg_idx], outs[return_idx])
