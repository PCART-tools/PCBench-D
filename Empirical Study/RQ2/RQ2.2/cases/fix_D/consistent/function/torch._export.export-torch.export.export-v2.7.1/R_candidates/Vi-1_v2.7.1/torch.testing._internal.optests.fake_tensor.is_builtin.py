def is_builtin(op):
    return op.namespace in ('aten', 'prims', 'prim')
