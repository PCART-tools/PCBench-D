@dispatch(ImmutableDenseMatrix, ImmutableDenseMatrix)
def _eval_is_eq(lhs, rhs): # noqa:F811
    """Helper method for Equality with matrices.sympy.

    Relational automatically converts matrices to ImmutableDenseMatrix
    instances, so this method only applies here.  Returns True if the
    matrices are definitively the same, False if they are definitively
    different, and None if undetermined (e.g. if they contain Symbols).
    Returning None triggers default handling of Equalities.

    """
    if lhs.shape != rhs.shape:
        return False
    return (lhs - rhs).is_zero_matrix
