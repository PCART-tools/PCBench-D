@dispatch(MatrixExpr, MatrixExpr)  # type: ignore
def _eval_is_eq(lhs, rhs): # noqa:F811
    if lhs.shape != rhs.shape:
        return False
    if (lhs - rhs).is_ZeroMatrix:
        return True
