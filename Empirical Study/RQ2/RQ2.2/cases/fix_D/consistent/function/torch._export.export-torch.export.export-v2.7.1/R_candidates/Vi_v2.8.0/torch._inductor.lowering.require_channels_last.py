def require_channels_last(_, *args, **kwargs):
    args, kwargs = pytree.tree_map_only(
        ir.IRNode, ir.ExternKernel.require_channels_last, (args, kwargs)
    )
    return args, kwargs
