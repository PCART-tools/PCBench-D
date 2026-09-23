def nsum(f, a, b, *, step=1, args=(), log=False, maxterms=int(2**20), tolerances=None):
    r"""Evaluate a convergent finite or infinite series.

    For finite `a` and `b`, this evaluates::

        f(a + np.arange(n)*step).sum()

    where ``n = int((b - a) / step) + 1``, where `f` is smooth, positive, and
    unimodal. The number of terms in the sum may be very large or infinite,
    in which case a partial sum is evaluated directly and the remainder is
    approximated using integration.

    Parameters
    ----------
    f : callable
        The function that evaluates terms to be summed. The signature must be::

            f(x: ndarray, *args) -> ndarray

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with ``x``.

        `f` must be an elementwise function: each element ``f(x)[i]``
        must equal ``f(x[i])`` for all indices ``i``. It must not mutate the
        array ``x`` or the arrays in ``args``, and it must return NaN where
        the argument is NaN.

        `f` must represent a smooth, positive, unimodal function of `x` defined at
        *all reals* between `a` and `b`.
    a, b : float array_like
        Real lower and upper limits of summed terms. Must be broadcastable.
        Each element of `a` must be less than the corresponding element in `b`.
    step : float array_like
        Finite, positive, real step between summed terms. Must be broadcastable
        with `a` and `b`. Note that the number of terms included in the sum will
        be ``floor((b - a) / step)`` + 1; adjust `b` accordingly to ensure
        that ``f(b)`` is included if intended.
    args : tuple of array_like, optional
        Additional positional arguments to be passed to `f`. Must be arrays
        broadcastable with `a`, `b`, and `step`. If the callable to be summed
        requires arguments that are not broadcastable with `a`, `b`, and `step`,
        wrap that callable with `f` such that `f` accepts only `x` and
        broadcastable ``*args``. See Examples.
    log : bool, default: False
        Setting to True indicates that `f` returns the log of the terms
        and that `atol` and `rtol` are expressed as the logs of the absolute
        and relative errors. In this case, the result object will contain the
        log of the sum and error. This is useful for summands for which
        numerical underflow or overflow would lead to inaccuracies.
    maxterms : int, default: 2**20
        The maximum number of terms to evaluate for direct summation.
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
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. (The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.)

        success : bool
            ``True`` when the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : Element(s) of `a`, `b`, or `step` are invalid
            - ``-2`` : Numerical integration reached its iteration limit;
              the sum may be divergent.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : The magnitude of the last term of the partial sum exceeds
              the tolerances, so the error estimate exceeds the tolerances.
              Consider increasing `maxterms` or loosening `tolerances`.
              Alternatively, the callable may not be unimodal, or the limits of
              summation may be too far from the function maximum. Consider
              increasing `maxterms` or breaking the sum into pieces.

        sum : float array
            An estimate of the sum.
        error : float array
            An estimate of the absolute error, assuming all terms are non-negative,
            the function is computed exactly, and direct summation is accurate to
            the precision of the result dtype.
        nfev : int array
            The number of points at which `f` was evaluated.

    See Also
    --------
    mpmath.nsum

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
    numerical integration. Note that the integral approximations may require
    evaluation of the function at points besides those that appear in the sum,
    so `f` must be a continuous and monotonically decreasing function defined
    for all reals within the integration interval. However, due to the nature
    of the integral approximation, the shape of the function between points
    that appear in the sum has little effect. If there is not a natural
    extension of the function to all reals, consider using linear interpolation,
    which is easy to evaluate and preserves monotonicity.

    The approach described above is generalized for non-unit
    `step` and finite `b` that is too large for direct evaluation of the sum,
    i.e. ``b - a + 1 > maxterms``. It is further generalized to unimodal
    functions by directly summing terms surrounding the maximum.
    This strategy may fail:

    - If the left limit is finite and the maximum is far from it.
    - If the right limit is finite and the maximum is far from it.
    - If both limits are finite and the maximum is far from the origin.

    In these cases, accuracy may be poor, and `nsum` may return status code ``4``.

    Although the callable `f` must be non-negative and unimodal,
    `nsum` can be used to evaluate more general forms of series. For instance, to
    evaluate an alternating series, pass a callable that returns the difference
    between pairs of adjacent terms, and adjust `step` accordingly. See Examples.

    References
    ----------
    .. [1] Wikipedia. "Integral test for convergence."
           https://en.wikipedia.org/wiki/Integral_test_for_convergence

    Examples
    --------
    Compute the infinite sum of the reciprocals of squared integers.

    >>> import numpy as np
    >>> from scipy.integrate import nsum
    >>> res = nsum(lambda k: 1/k**2, 1, np.inf)
    >>> ref = np.pi**2/6  # true value
    >>> res.error  # estimated error
    np.float64(7.448762306416137e-09)
    >>> (res.sum - ref)/ref  # true error
    np.float64(-1.839871898894426e-13)
    >>> res.nfev  # number of points at which callable was evaluated
    np.int32(8561)

    Compute the infinite sums of the reciprocals of integers raised to powers ``p``,
    where ``p`` is an array.

    >>> from scipy import special
    >>> p = np.arange(3, 10)
    >>> res = nsum(lambda k, p: 1/k**p, 1, np.inf, maxterms=1e3, args=(p,))
    >>> ref = special.zeta(p, 1)
    >>> np.allclose(res.sum, ref)
    True

    Evaluate the alternating harmonic series.

    >>> res = nsum(lambda x: 1/x - 1/(x+1), 1, np.inf, step=2)
    >>> res.sum, res.sum - np.log(2)  # result, difference vs analytical sum
    (np.float64(0.6931471805598691), np.float64(-7.616129948928574e-14))

    """ # noqa: E501
    # Potential future work:
    # - improve error estimate of `_direct` sum
    # - add other methods for convergence acceleration (Richardson, epsilon)
    # - support negative monotone increasing functions?
    # - b < a / negative step?
    # - complex-valued function?
    # - check for violations of monotonicity?

    # Function-specific input validation / standardization
    tmp = _nsum_iv(f, a, b, step, args, log, maxterms, tolerances)
    f, a, b, step, valid_abstep, args, log, maxterms, atol, rtol, xp = tmp

    # Additional elementwise algorithm input validation / standardization
    tmp = eim._initialize(f, (a,), args, complex_ok=False, xp=xp)
    f, xs, fs, args, shape, dtype, xp = tmp

    # Finish preparing `a`, `b`, and `step` arrays
    a = xs[0]
    b = xp.astype(xp_ravel(xp.broadcast_to(b, shape)), dtype)
    step = xp.astype(xp_ravel(xp.broadcast_to(step, shape)), dtype)
    valid_abstep = xp_ravel(xp.broadcast_to(valid_abstep, shape))
    nterms = xp.floor((b - a) / step)
    finite_terms = xp.isfinite(nterms)
    b[finite_terms] = a[finite_terms] + nterms[finite_terms]*step[finite_terms]

    # Define constants
    eps = xp.finfo(dtype).eps
    zero = xp.asarray(-xp.inf if log else 0, dtype=dtype)[()]
    if rtol is None:
        rtol = 0.5*math.log(eps) if log else eps**0.5
    constants = (dtype, log, eps, zero, rtol, atol, maxterms)

    # Prepare result arrays
    S = xp.empty_like(a)
    E = xp.empty_like(a)
    status = xp.zeros(len(a), dtype=xp.int32)
    nfev = xp.ones(len(a), dtype=xp.int32)  # one function evaluation above

    # Branch for direct sum evaluation / integral approximation / invalid input
    i0 = ~valid_abstep                     # invalid
    i1 = (nterms + 1 <= maxterms) & ~i0    # direct sum evaluation
    i2 = xp.isfinite(a) & ~i1 & ~i0        # infinite sum to the right
    i3 = xp.isfinite(b) & ~i2 & ~i1 & ~i0  # infinite sum to the left
    i4 = ~i3 & ~i2 & ~i1 & ~i0             # infinite sum on both sides

    if xp.any(i0):
        S[i0], E[i0] = xp.nan, xp.nan
        status[i0] = -1

    if xp.any(i1):
        args_direct = [arg[i1] for arg in args]
        tmp = _direct(f, a[i1], b[i1], step[i1], args_direct, constants, xp)
        S[i1], E[i1] = tmp[:-1]
        nfev[i1] += tmp[-1]
        status[i1] = -3 * xp.asarray(~xp.isfinite(S[i1]), dtype=xp.int32)

    if xp.any(i2):
        args_indirect = [arg[i2] for arg in args]
        tmp = _integral_bound(f, a[i2], b[i2], step[i2],
                              args_indirect, constants, xp)
        S[i2], E[i2], status[i2] = tmp[:-1]
        nfev[i2] += tmp[-1]

    if xp.any(i3):
        args_indirect = [arg[i3] for arg in args]
        def _f(x, *args): return f(-x, *args)
        tmp = _integral_bound(_f, -b[i3], -a[i3], step[i3],
                              args_indirect, constants, xp)
        S[i3], E[i3], status[i3] = tmp[:-1]
        nfev[i3] += tmp[-1]

    if xp.any(i4):
        args_indirect = [arg[i4] for arg in args]

        # There are two obvious high-level strategies:
        # - Do two separate half-infinite sums (e.g. from -inf to 0 and 1 to inf)
        # - Make a callable that returns f(x) + f(-x) and do a single half-infinite sum
        # I thought the latter would have about half the overhead, so I went that way.
        # Then there are two ways of ensuring that f(0) doesn't get counted twice.
        # - Evaluate the sum from 1 to inf and add f(0)
        # - Evaluate the sum from 0 to inf and subtract f(0)
        # - Evaluate the sum from 0 to inf, but apply a weight of 0.5 when `x = 0`
        # The last option has more overhead, but is simpler to implement correctly
        # (especially getting the status message right)
        if log:
            def _f(x, *args):
                log_factor = xp.where(x==0, math.log(0.5), 0)
                out = xp.stack([f(x, *args), f(-x, *args)], axis=0)
                return special.logsumexp(out, axis=0) + log_factor

        else:
            def _f(x, *args):
                factor = xp.where(x==0, 0.5, 1)
                return (f(x, *args) + f(-x, *args)) * factor

        zero = xp.zeros_like(a[i4])
        tmp = _integral_bound(_f, zero, b[i4], step[i4], args_indirect, constants, xp)
        S[i4], E[i4], status[i4] = tmp[:-1]
        nfev[i4] += 2*tmp[-1]

    # Return results
    S, E = S.reshape(shape)[()], E.reshape(shape)[()]
    status, nfev = status.reshape(shape)[()], nfev.reshape(shape)[()]
    return _RichResult(sum=S, error=E, status=status, success=status == 0,
                       nfev=nfev)
