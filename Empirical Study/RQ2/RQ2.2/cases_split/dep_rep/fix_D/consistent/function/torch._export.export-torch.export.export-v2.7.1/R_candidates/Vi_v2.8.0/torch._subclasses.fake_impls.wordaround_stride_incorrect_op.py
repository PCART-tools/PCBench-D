@register_op_impl(stride_incorrect_op)
def wordaround_stride_incorrect_op(fake_mode, func, *args, **kwargs):
    # This is a workaround for meta implmentations with incorrect strides

    def is_symbolic(x):
        if isinstance(x, FakeTensor):
            return x._has_symbolic_sizes_strides
        if isinstance(x, (torch.SymInt, torch.SymFloat, torch.SymBool)):
            return True
        return False

    # For static shapes, we can fall back to eager for the real strides
    if fake_mode.allow_fallback_kernels:
        require_dynamic = any(
            is_symbolic(x) for x in itertools.chain(args, kwargs.values())
        )
        if not require_dynamic:
            flat_args, args_spec = pytree.tree_flatten((args, kwargs))
            return run_fallback_kernel(fake_mode, func, flat_args, args_spec, None)

    raise UnsupportedOperatorException(func)
