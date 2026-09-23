def idd_findrank(eps, m, n, matvect):
    """
    Estimate rank of a real matrix to a specified relative precision using
    random matrix-vector multiplication.

    :param eps:
        Relative precision.
    :type eps: float
    :param m:
        Matrix row dimension.
    :type m: int
    :param n:
        Matrix column dimension.
    :type n: int
    :param matvect:
        Function to apply the matrix transpose to a vector, with call signature
        `y = matvect(x)`, where `x` and `y` are the input and output vectors,
        respectively.
    :type matvect: function

    :return:
        Rank estimate.
    :rtype: int
    """
    k, ra, ier = _id.idd_findrank(eps, m, n, matvect)
    if ier:
        raise _RETCODE_ERROR
    return k
