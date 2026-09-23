@array_function_dispatch(_unary_dispatcher)
def sqrt(x):
    """
    Compute the square root of x.

    For negative input elements, a complex value is returned
    (unlike `numpy.sqrt` which returns NaN).

    Parameters
    ----------
    x : array_like
       The input value(s).

    Returns
    -------
    out : ndarray or scalar
       The square root of `x`. If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.sqrt

    Examples
    --------
    For real, non-negative inputs this works just like `numpy.sqrt`:

    >>> np.emath.sqrt(1)
    1.0
    >>> np.emath.sqrt([1, 4])
    array([1.,  2.])

    But it automatically handles negative inputs:

    >>> np.emath.sqrt(-1)
    1j
    >>> np.emath.sqrt([-1,4])
    array([0.+1.j, 2.+0.j])

    Different results are expected because:
    floating point 0.0 and -0.0 are distinct.

    For more control, explicitly use complex() as follows:

    >>> np.emath.sqrt(complex(-4.0, 0.0))
    2j
    >>> np.emath.sqrt(complex(-4.0, -0.0))
    -2j
    """
    x = _fix_real_lt_zero(x)
    return nx.sqrt(x)
