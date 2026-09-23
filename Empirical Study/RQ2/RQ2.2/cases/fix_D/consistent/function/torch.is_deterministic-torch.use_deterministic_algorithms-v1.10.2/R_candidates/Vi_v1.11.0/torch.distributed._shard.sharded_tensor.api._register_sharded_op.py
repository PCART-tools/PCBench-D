def _register_sharded_op(op, func):
    from inspect import signature
    if len(signature(func).parameters) != 4:
        raise TypeError(
            f'Custom sharded op function expects signature: '
            f'(types, args, kwargs, process_group), but received '
            f'signature: {signature(func)}')

    global _SHARDED_OPS
    _SHARDED_OPS[op] = func
