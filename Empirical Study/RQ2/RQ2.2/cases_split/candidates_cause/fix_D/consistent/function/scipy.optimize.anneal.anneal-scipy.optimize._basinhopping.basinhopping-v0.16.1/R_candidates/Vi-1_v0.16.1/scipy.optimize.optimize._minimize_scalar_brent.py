def _minimize_scalar_brent(func, brack=None, args=(),
                           xtol=1.48e-8, maxiter=500,
                           **unknown_options):
    """
    Options
    -------
    maxiter : int
        Maximum number of iterations to perform.
    xtol : float
        Relative error in solution `xopt` acceptable for convergence.

    Notes
    -----
    Uses inverse parabolic interpolation when possible to speed up
    convergence of golden section method.

    """
    _check_unknown_options(unknown_options)
    tol = xtol
    if tol < 0:
        raise ValueError('tolerance should be >= 0, got %r' % tol)

    brent = Brent(func=func, args=args, tol=tol,
                  full_output=True, maxiter=maxiter)
    brent.set_bracket(brack)
    brent.optimize()
    x, fval, nit, nfev = brent.get_result(full_output=True)
    return OptimizeResult(fun=fval, x=x, nit=nit, nfev=nfev)
