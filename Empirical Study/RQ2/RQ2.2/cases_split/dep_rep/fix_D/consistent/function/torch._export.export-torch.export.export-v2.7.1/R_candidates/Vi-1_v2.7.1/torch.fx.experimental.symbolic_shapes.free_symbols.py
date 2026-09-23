def free_symbols(val: IterateExprs) -> OrderedSet[sympy.Symbol]:
    if val is None:
        return OrderedSet()
    itr = _iterate_exprs(val)
    # we need at least 1 to call union, so we hand code the identity
    try:
        first_expr = next(itr)
    except StopIteration:
        return OrderedSet()

    # TODO: Apparently, returning an OrderedSet here breaks
    # python test/distributed/tensor/test_dtensor_compile.py TestDTensorCompile.test_dtensor_dynamic
    return first_expr.free_symbols.union(*(e.free_symbols for e in itr))  # type: ignore[return-value]
