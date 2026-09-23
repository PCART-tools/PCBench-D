@array_function_dispatch(_unary_dispatcher)
def arccos(x):
    """
    Compute the inverse cosine of x.

    Return the "principal value" (for a description of this, see
    `numpy.arccos`) of the inverse cosine of `x`. For real `x` such that
    `abs(x) <= 1`, this is a real number in the closed interval
    :math:`[0, \\pi]`.  Otherwise, the complex principle value is returned.

    Parameters
    ----------
    x : array_like or scalar
       The value(s) whose arccos is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The inverse cosine(s) of the `x` value(s). If `x` was a scalar, so
       is `out`, otherwise an array object is returned.

    See Also
    --------
    numpy.arccos

    Notes
    -----
    For an arccos() that returns ``NAN`` when real `x` is not in the
    interval ``[-1,1]``, use `numpy.arccos`.

    Examples
    --------
    >>> np.set_printoptions(precision=4)

    >>> np.emath.arccos(1) # a scalar is returned
    0.0

    >>> np.emath.arccos([1,2])
    array([0.-0.j   , 0.-1.317j])

    """
    x = _fix_real_abs_gt_1(x)
    return nx.arccos(x)
