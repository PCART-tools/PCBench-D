def has_effects(op, args, kwargs) -> bool:
    # Skip over the profiler's RecordFunction as they should not show up in the graph
    _skip_ops = {torch.ops.profiler._record_function_exit._RecordFunction}
    if op in _skip_ops:
        return False

    return (
        isinstance(op, (torch._ops.HigherOrderOperator, torch._ops.OpOverload))
        and not has_aliasing(op)
        and get_effect_key(op, args, kwargs) is not None
    )
