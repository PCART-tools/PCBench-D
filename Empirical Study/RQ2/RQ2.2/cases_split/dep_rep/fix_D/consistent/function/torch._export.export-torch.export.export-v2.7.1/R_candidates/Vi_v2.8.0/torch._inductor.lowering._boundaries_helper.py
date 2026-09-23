def _boundaries_helper(tb: TensorBox) -> tuple[str, sympy.Expr, sympy.Expr, sympy.Expr]:
    return (
        tb.get_name(),
        tb.get_size()[-1],
        tb.get_size()[0] * tb.get_stride()[0],
        tb.get_stride()[-1],
    )
