@array_function_dispatch(_unary_dispatcher)
def arcsin(x):
    """
    Compute the inverse sine of x.

    Return the "principal value" (for a description of this, see
    `numpy.arcsin`) of the inverse sine of `x`. For real `x` such that
    `abs(x) <= 1`, this is a real number in the closed interval
    :math:`[-\\pi/2, \\pi/2]`.  Otherwise, the complex principle value is
    returned.

    Parameters
    ----------
    x : array_like or scalar
       The value(s) whose arcsin is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The inverse sine(s) of the `x` value(s). If `x` was a scalar, so
       is `out`, otherwise an array object is returned.

    See Also
    --------
    numpy.arcsin

    Notes
    -----
    For an arcsin() that returns ``NAN`` when real `x` is not in the
    interval ``[-1,1]``, use `numpy.arcsin`.

    Examples
    --------
    >>> np.set_printoptions(precision=4)

    >>> np.emath.arcsin(0)
    0.0

    >>> np.emath.arcsin([0,1])
    array([0.    , 1.5708])

    """
    x = _fix_real_abs_gt_1(x)
    return nx.arcsin(x)
