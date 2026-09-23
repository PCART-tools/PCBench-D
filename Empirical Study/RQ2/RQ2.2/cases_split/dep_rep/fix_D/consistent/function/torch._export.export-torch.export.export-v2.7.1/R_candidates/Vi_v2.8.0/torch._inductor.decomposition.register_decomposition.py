def register_decomposition(
    ops: Union[_GenericOperator, list[_GenericOperator]],
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    for op in ops if isinstance(ops, list) else [ops]:
        if op in decompositions:
            log.warning("duplicate decomp: %s", ops)
    return decomp.register_decomposition(ops, decompositions)
