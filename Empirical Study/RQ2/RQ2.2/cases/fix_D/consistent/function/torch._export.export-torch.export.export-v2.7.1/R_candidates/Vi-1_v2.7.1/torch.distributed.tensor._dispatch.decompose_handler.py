def decompose_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    """
    Decomposes a op to core ATen op, this handler is mostly here
    for inference mode usage where the ops are not core aten ops.
    """
    r = op_call.decompose(*args, **kwargs)
    if r is not NotImplemented:
        return r
    else:
        raise RuntimeError("Decomposition failed")
