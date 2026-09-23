def _is_view_op(tgt):
    if tgt is not None and isinstance(tgt, torch._ops.OpOverload):
        schema = tgt._schema
        if len(schema.arguments) > 0:
            first_arg = schema.arguments[0]
            # check if op is a view
            return (
                first_arg.alias_info is not None and not first_arg.alias_info.is_write
            )
