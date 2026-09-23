def is_builtin(op: OpOverload) -> bool:
    assert isinstance(op, OpOverload)
    return op.namespace in {"aten", "prim", "prims"}
