def _is_out_variant_op(op: OpOverload):
    # simple analysis of function schema to determine
    # if this is an out variant, it might not
    # be entirely correct, but it's good enough for now.
    return "out" in op._schema.overload_name
