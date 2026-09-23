def _nsum(f, a, b, step=1, args=(), log=False, maxterms=int(2**20), atol=None,
          rtol=None):
    r"""Evaluate a convergent sum.

    For finite `b`, this evaluates::

        f(a + np.arange(n)*step).sum()

    where ``n = int((b - a) / step) + 1``. If `f` is smooth, positive, and
    monotone decreasing, `b` may be infinite, in which case the infinite sum
    is approximated using integration.

    Parameters
    ----------
    f : callable
        The function that evaluates terms to be summed. The signature must be::

            f(x: ndarray, *args) -> ndarray

         where each element of ``x`` is a finite real and ``args`` is a tuple,
         which may contain an arbitrary number of arrays that are broadcastable
         with `x`. `f` must represent a smooth, positive, and monotone decreasing
         function of `x`; `_nsum` performs no checks to verify that these conditions
         are met and may return erroneous results if they are violated.
    a, b : array_like
        Real lower and upper limits of summed terms. Must be broadcastable.
        Each element of `a` must be finite and less than the corresponding
        element in `b`, but elements of `b` may be infinite.
    step : array_like
        Finite, positive, real step between summed terms. Must be broadcastable
        with `a` and `b`.
    args : tuple, optional
        Additional positional arguments to be passed to `f`. Must be arrays
        broadcastable with `a`, `b`, and `step`. If the callable to be summed
        requires arguments that are not broadcastable with `a`, `b`, and `step`,
        wrap that callable with `f`. See Examples.
    log : bool, default: False
        Setting to True indicates that `f` returns the log of the terms
        and that `atol` and `rtol` are expressed as the logs of the absolute
        and relative errors. In this case, the result object will contain the
        log of the sum and error. This is useful for summands for which
        numerical underflow or overflow would lead to inaccuracies.
    maxterms : int, default: 2**32
        The maximum number of terms to evaluate when summing directly. 
        Additional function evaluations may be performed for input
        validation and integral evaluation. 
    atol, rtol : float, optional
        Absolute termination tolerance (default: 0) and relative termination
        tolerance (default: ``eps**0.5``, where ``eps`` is the precision of
        the result dtype), respectively. Must be non-negative
        and finite if `log` is False, and must be expressed as the log of a
        non-negative and finite number if `log` is True.

    Returns
    -------
    res : _RichResult
        An instance of `scipy._lib._util._RichResult` with the following
        attributes. (The descriptions are written as though the values will be
        scalars; however, if `func` returns an array, the outputs will be

        arrays of the same shape.)
        success : bool
            ``True`` when the algorithm terminated successfully (status ``0``).
        status : int
            An integer representing the exit status of the algorithm.
            ``0`` : The algorithm converged to the specified tolerances.
            ``-1`` : Element(s) of `a`, `b`, or `step` are invalid
            ``-2`` : Numerical integration reached its iteration limit; the sum may be divergent.
            ``-3`` : A non-finite value was encountered.
        sum : float
            An estimate of the sum.
        error : float
            An estimate of the absolute error, assuming all terms are non-negative.
        nfev : int
            The number of points at which `func` was evaluated.

    See Also
    --------
    tanhsinh

    Notes
    -----
    The method implemented for infinite summation is related to the integral
    test for convergence of an infinite series: assuming `step` size 1 for
    simplicity of exposition, the sum of a monotone decreasing function is bounded by

    .. math::

        \int_u^\infty f(x) dx \leq \sum_{k=u}^\infty f(k) \leq \int_u^\infty f(x) dx + f(u)

    Let :math:`a` represent  `a`, :math:`n` represent `maxterms`, :math:`\epsilon_a`
    represent `atol`, and :math:`\epsilon_r` represent `rtol`.
    The implementation first evaluates the integral :math:`S_l=\int_a^\infty f(x) dx`
    as a lower bound of the infinite sum. Then, it seeks a value :math:`c > a` such
    that :math:`f(c) < \epsilon_a + S_l \epsilon_r`, if it exists; otherwise,
    let :math:`c = a + n`. Then the infinite sum is approximated as
    
    .. math::

        \sum_{k=a}^{c-1} f(k) + \int_c^\infty f(x) dx + f(c)/2

    and the reported error is :math:`f(c)/2` plus the error estimate of
    numerical integration. The approach described above is generalized for non-unit
    `step` and finite `b` that is too large for direct evaluation of the sum,
    i.e. ``b - a + 1 > maxterms``.

    References
    ----------
    [1] Wikipedia. "Integral test for convergence."
    https://en.wikipedia.org/wiki/Integral_test_for_convergence

    Examples
    --------
    Compute the infinite sum of the reciprocals of squared integers.
    
    >>> import numpy as np
    >>> from scipy.integrate._tanhsinh import _nsum
    >>> res = _nsum(lambda k: 1/k**2, 1, np.inf, maxterms=1e3)
    >>> ref = np.pi**2/6  # true value
    >>> res.error  # estimated error
    4.990014980029223e-07
    >>> (res.sum - ref)/ref  # true error
    -1.0101760641302586e-10
    >>> res.nfev  # number of points at which callable was evaluated
    1142
    
    Compute the infinite sums of the reciprocals of integers raised to powers ``p``.
    
    >>> from scipy import special
    >>> p = np.arange(2, 10)
    >>> res = _nsum(lambda k, p: 1/k**p, 1, np.inf, maxterms=1e3, args=(p,))
    >>> ref = special.zeta(p, 1)
    >>> np.allclose(res.sum, ref)
    True
    
    """ # noqa: E501
    # Potential future work:
    # - more careful testing of when `b` is slightly less than `a` plus an
    #   integer multiple of step (needed before this is public)
    # - improve error estimate of `_direct` sum
    # - add other methods for convergence acceleration (Richardson, epsilon)
    # - support infinite lower limit?
    # - support negative monotone increasing functions?
    # - b < a / negative step?
    # - complex-valued function?
    # - check for violations of monotonicity?

    # Function-specific input validation / standardization
    tmp = _nsum_iv(f, a, b, step, args, log, maxterms, atol, rtol)
    f, a, b, step, valid_abstep, args, log, maxterms, atol, rtol = tmp

    # Additional elementwise algorithm input validation / standardization
    tmp = eim._initialize(f, (a,), args, complex_ok=False)
    f, xs, fs, args, shape, dtype, xp = tmp

    # Finish preparing `a`, `b`, and `step` arrays
    a = xs[0]
    b = np.broadcast_to(b, shape).ravel().astype(dtype)
    step = np.broadcast_to(step, shape).ravel().astype(dtype)
    valid_abstep = np.broadcast_to(valid_abstep, shape).ravel()
    nterms = np.floor((b - a) / step)
    b = a + nterms*step

    # Define constants
    eps = np.finfo(dtype).eps
    zero = np.asarray(-np.inf if log else 0, dtype=dtype)[()]
    if rtol is None:
        rtol = 0.5*np.log(eps) if log else eps**0.5
    constants = (dtype, log, eps, zero, rtol, atol, maxterms)

    # Prepare result arrays
    S = np.empty_like(a)
    E = np.empty_like(a)
    status = np.zeros(len(a), dtype=int)
    nfev = np.ones(len(a), dtype=int)  # one function evaluation above

    # Branch for direct sum evaluation / integral approximation / invalid input
    i1 = (nterms + 1 <= maxterms) & valid_abstep
    i2 = (nterms + 1 > maxterms) & valid_abstep
    i3 = ~valid_abstep

    if np.any(i1):
        args_direct = [arg[i1] for arg in args]
        tmp = _direct(f, a[i1], b[i1], step[i1], args_direct, constants)
        S[i1], E[i1] = tmp[:-1]
        nfev[i1] += tmp[-1]
        status[i1] = -3 * (~np.isfinite(S[i1]))

    if np.any(i2):
        args_indirect = [arg[i2] for arg in args]
        tmp = _integral_bound(f, a[i2], b[i2], step[i2], args_indirect, constants)
        S[i2], E[i2], status[i2] = tmp[:-1]
        nfev[i2] += tmp[-1]

    if np.any(i3):
        S[i3], E[i3] = np.nan, np.nan
        status[i3] = -1

    # Return results
    S, E = S.reshape(shape)[()], E.reshape(shape)[()]
    status, nfev = status.reshape(shape)[()], nfev.reshape(shape)[()]
    return _RichResult(sum=S, error=E, status=status, success=status == 0,
                       nfev=nfev)
