def statically_known_true(
    shape_env: ShapeEnv,
    expr: Union[sympy.Basic, bool],
    axioms: Optional[tuple[sympy.Expr]] = None,
    var_to_range: Optional[tuple[tuple[sympy.Symbol, ValueRanges[Any]]]] = None,
) -> bool:
    if expr in (True, False):
        return bool(expr)

    try:
        simplified = shape_env._maybe_evaluate_static(
            expr,
            axioms=axioms,
            var_to_range=var_to_range,
        )
        if simplified is not None:
            return bool(simplified)
    except Exception:
        log.debug("Could not simplify  %s", expr, exc_info=True)

    return False
