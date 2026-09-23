def _constrain_symbol_range(
    shape_env: ShapeEnv, s: sympy.Symbol, compiler_min: int, compiler_max: int
) -> None:
    shape_env.constrain_symbol_range(s, compiler_min, compiler_max)
