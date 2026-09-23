def has_free_symbols(itr: Iterable[Any]) -> bool:
    return any(isinstance(x, sympy.Expr) and not x.is_number for x in itr)
