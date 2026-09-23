def get_hint(v: Union[sympy.Expr, int]) -> int:
    if isinstance(v, int):
        return v
    else:
        return V.graph.sizevars.size_hint(v, fallback=config.unbacked_symint_fallback)
