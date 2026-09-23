def brent(func, args=(), brack=None, tol=1.48e-8, full_output=0, maxiter=500):
    """
    Given a function of one-variable and a possible bracketing interval,
    return the minimum of the function isolated to a fractional precision of
    tol.

    Parameters
    ----------
    func : callable f(x,*args)
        Objective function.
    args : tuple, optional
        Additional arguments (if present).
    brack : tuple, optional
        Either a triple (xa,xb,xc) where xa<xb<xc and func(xb) <
        func(xa), func(xc) or a pair (xa,xb) which are used as a
        starting interval for a downhill bracket search (see
        `bracket`). Providing the pair (xa,xb) does not always mean
        the obtained solution will satisfy xa<=x<=xb.
    tol : float, optional
        Stop if between iteration change is less than `tol`.
    full_output : bool, optional
        If True, return all output args (xmin, fval, iter,
        funcalls).
    maxiter : int, optional
        Maximum number of iterations in solution.

    Returns
    -------
    xmin : ndarray
        Optimum point.
    fval : float
        Optimum value.
    iter : int
        Number of iterations.
    funcalls : int
        Number of objective function evaluations made.

    See also
    --------
    minimize_scalar: Interface to minimization algorithms for scalar
        univariate functions. See the 'Brent' `method` in particular.

    Notes
    -----
    Uses inverse parabolic interpolation when possible to speed up
    convergence of golden section method.

    """
    options = {'xtol': tol,
               'maxiter': maxiter}
    res = _minimize_scalar_brent(func, brack, args, **options)
    if full_output:
        return res['x'], res['fun'], res['nit'], res['nfev']
    else:
        return res['x']
