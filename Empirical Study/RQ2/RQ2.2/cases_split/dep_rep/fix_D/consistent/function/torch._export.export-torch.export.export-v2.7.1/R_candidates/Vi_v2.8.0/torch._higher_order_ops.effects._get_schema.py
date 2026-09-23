def _get_schema(op, args) -> torch.FunctionSchema:
    if isinstance(op, torch._ops.OpOverload):
        return op._schema
    elif op == call_torchbind:
        return getattr(args[0], args[1]).schema
    else:
        raise RuntimeError(f"Unable to get schema for op {op}")
