@array_function_dispatch(_unary_dispatcher)
def log(x):
    """
    Compute the natural logarithm of `x`.

    Return the "principal value" (for a description of this, see `numpy.log`)
    of :math:`log_e(x)`. For real `x > 0`, this is a real number (``log(0)``
    returns ``-inf`` and ``log(np.inf)`` returns ``inf``). Otherwise, the
    complex principle value is returned.

    Parameters
    ----------
    x : array_like
       The value(s) whose log is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The log of the `x` value(s). If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.log

    Notes
    -----
    For a log() that returns ``NAN`` when real `x < 0`, use `numpy.log`
    (note, however, that otherwise `numpy.log` and this `log` are identical,
    i.e., both return ``-inf`` for `x = 0`, ``inf`` for `x = inf`, and,
    notably, the complex principle value if ``x.imag != 0``).

    Examples
    --------
    >>> np.emath.log(np.exp(1))
    1.0

    Negative arguments are handled "correctly" (recall that
    ``exp(log(x)) == x`` does *not* hold for real ``x < 0``):

    >>> np.emath.log(-np.exp(1)) == (1 + np.pi * 1j)
    True

    """
    x = _fix_real_lt_zero(x)
    return nx.log(x)
