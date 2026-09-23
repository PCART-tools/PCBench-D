def in_namespace(op, namespace):
    if isinstance(op, torch._ops.OpOverloadPacket):
        return namespace in op._qualified_op_name
    elif isinstance(op, torch._ops.OpOverload):
        return namespace in op.name()
    return False
