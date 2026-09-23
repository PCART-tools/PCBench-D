@array_function_dispatch(_power_dispatcher)
def power(x, p):
    """
    Return x to the power p, (x**p).

    If `x` contains negative values, the output is converted to the
    complex domain.

    Parameters
    ----------
    x : array_like
        The input value(s).
    p : array_like of ints
        The power(s) to which `x` is raised. If `x` contains multiple values,
        `p` has to either be a scalar, or contain the same number of values
        as `x`. In the latter case, the result is
        ``x[0]**p[0], x[1]**p[1], ...``.

    Returns
    -------
    out : ndarray or scalar
        The result of ``x**p``. If `x` and `p` are scalars, so is `out`,
        otherwise an array is returned.

    See Also
    --------
    numpy.power

    Examples
    --------
    >>> np.set_printoptions(precision=4)

    >>> np.emath.power([2, 4], 2)
    array([ 4, 16])
    >>> np.emath.power([2, 4], -2)
    array([0.25  ,  0.0625])
    >>> np.emath.power([-2, 4], 2)
    array([ 4.-0.j, 16.+0.j])

    """
    x = _fix_real_lt_zero(x)
    p = _fix_int_lt_zero(p)
    return nx.power(x, p)
