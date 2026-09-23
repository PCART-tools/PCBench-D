@array_function_dispatch(_unary_dispatcher)
def log2(x):
    """
    Compute the logarithm base 2 of `x`.

    Return the "principal value" (for a description of this, see
    `numpy.log2`) of :math:`log_2(x)`. For real `x > 0`, this is
    a real number (``log2(0)`` returns ``-inf`` and ``log2(np.inf)`` returns
    ``inf``). Otherwise, the complex principle value is returned.

    Parameters
    ----------
    x : array_like
       The value(s) whose log base 2 is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The log base 2 of the `x` value(s). If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.log2

    Notes
    -----
    For a log2() that returns ``NAN`` when real `x < 0`, use `numpy.log2`
    (note, however, that otherwise `numpy.log2` and this `log2` are
    identical, i.e., both return ``-inf`` for `x = 0`, ``inf`` for `x = inf`,
    and, notably, the complex principle value if ``x.imag != 0``).

    Examples
    --------
    We set the printing precision so the example can be auto-tested:

    >>> np.set_printoptions(precision=4)

    >>> np.emath.log2(8)
    3.0
    >>> np.emath.log2([-4, -8, 8])
    array([2.+4.5324j, 3.+4.5324j, 3.+0.j    ])

    """
    x = _fix_real_lt_zero(x)
    return nx.log2(x)
