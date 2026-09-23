def require_contiguous(_, *args, **kwargs):
    args, kwargs = pytree.tree_map_only(
        ir.IRNode, ir.ExternKernel.require_contiguous, (args, kwargs)
    )
    return args, kwargs
