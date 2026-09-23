def require_dense(_, *args, **kwargs):
    args, kwargs = pytree.tree_map_only(
        ir.IRNode, ir.ExternKernel.require_stride1, (args, kwargs)
    )
    return args, kwargs
