def _iterate_exprs(val: IterateExprs) -> Iterator[sympy.Basic]:
    if isinstance(val, SymTypes):
        # This allow applies to the jagged layout NestedTensor case as
        # nested ints are not symbolic
        if is_symbolic(val):
            yield val.node.expr
    elif isinstance(val, sympy.Basic):
        yield val
    elif isinstance(val, (int, float, bool)):
        pass
    elif isinstance(val, (tuple, list)):
        for s in val:
            yield from _iterate_exprs(s)
    elif is_sparse_any(val):
        yield from _iterate_exprs(val.size())
    elif isinstance(val, torch.Tensor):
        yield from _iterate_exprs(val.size())
        yield from _iterate_exprs(val.stride())
        yield from _iterate_exprs(val.storage_offset())
    elif val is None:
        pass
    # see Note: [Generator arguments in AOTDispatcher]
    elif isinstance(val, torch.Generator):
        pass
    else:
        raise AssertionError(f"cannot extract sympy expressions from {val} {type(val)}")
