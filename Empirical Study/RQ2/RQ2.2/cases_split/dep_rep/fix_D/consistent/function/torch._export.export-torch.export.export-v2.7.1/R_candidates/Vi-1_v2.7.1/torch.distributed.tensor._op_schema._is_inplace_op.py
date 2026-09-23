def _is_inplace_op(op: OpOverload):
    # simple analysis of function schema to determine
    # if this is an inplace variant, it might not
    # be entirely correct, but it's good enough for now.
    return op._schema.name[-1] == "_"
