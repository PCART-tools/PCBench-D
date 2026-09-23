def _expr_lookup(namespace: str | None) -> set[tuple[str | None, str, tuple[str, ...]]]:
    """Create lookup of potential Expr methods (in the given namespace)."""
    # dummy Expr object that we can introspect
    expr = pl.Expr()
    expr._pyexpr = None

    # optional indirection to "expr.str", "expr.dt", etc
    if namespace is not None:
        expr = getattr(expr, namespace)

    lookup = set()
    for name in dir(expr):
        if not name.startswith("_"):
            try:
                m = getattr(expr, name)
            except AttributeError:  # may raise for @property methods
                continue
            if callable(m):
                # add function signature (argument names only) to the lookup
                # as a _possible_ candidate for expression-dispatch
                m = _undecorated(m)
                args = m.__code__.co_varnames[: m.__code__.co_argcount]
                lookup.add((namespace, name, args))
    return lookup
