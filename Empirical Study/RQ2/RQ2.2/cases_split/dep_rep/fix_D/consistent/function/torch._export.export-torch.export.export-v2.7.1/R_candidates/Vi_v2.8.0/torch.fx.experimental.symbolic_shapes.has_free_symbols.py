def has_free_symbols(val: IterateExprs) -> bool:
    """Faster version of bool(free_symbols(val))"""
    return not all((e.is_number or e.is_Boolean) for e in _iterate_exprs(val))
