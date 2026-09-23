def gradcheck_wrapper_triangular_input(op, input, *args, upper=False, **kwargs):
    """Gradcheck wrpper for functions that take lower or upper triangular matrices as input.

    They require a modified function because the finite-difference algorithm
    for calculating derivatives does not preserve the triangular property of the input.
    """
    return op(input.triu() if upper else input.tril(), upper)
