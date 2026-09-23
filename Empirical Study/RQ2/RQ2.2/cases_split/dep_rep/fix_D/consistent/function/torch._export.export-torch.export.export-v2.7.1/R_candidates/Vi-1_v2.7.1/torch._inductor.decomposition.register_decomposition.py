def register_decomposition(
    ops: list[Union[torch._ops.OperatorBase, torch._ops.OpOverloadPacket]],
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    for op in [ops] if callable(ops) else ops:  # type: ignore[attr-defined]
        if op in decompositions:
            log.warning("duplicate decomp: %s", ops)
    return decomp.register_decomposition(ops, decompositions)
