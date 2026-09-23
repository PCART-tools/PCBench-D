def expr_fits_within_32bit(e: sympy.Expr) -> bool:
    from .virtualized import V

    int_max = torch.iinfo(torch.int32).max
    size_hint = V.graph.sizevars.size_hint
    has_hint = V.graph.sizevars.shape_env.has_hint

    # Allow for unhinted e as long as we can still statically prove
    # (e.g., via ValueRanges) that it is still in bounds
    if V.graph.sizevars.statically_known_true(e <= int_max):
        return True
    # Otherwise, the hint MUST exist and be in range
    return has_hint(e) and size_hint(e) <= int_max
