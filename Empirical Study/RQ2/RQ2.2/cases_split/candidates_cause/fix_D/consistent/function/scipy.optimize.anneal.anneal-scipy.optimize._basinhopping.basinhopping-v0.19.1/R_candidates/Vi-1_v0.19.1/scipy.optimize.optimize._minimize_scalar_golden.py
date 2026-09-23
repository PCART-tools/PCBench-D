def _minimize_scalar_golden(func, brack=None, args=(),
                            xtol=_epsilon, maxiter=5000, **unknown_options):
    """
    Options
    -------
    maxiter : int
        Maximum number of iterations to perform.
    xtol : float
        Relative error in solution `xopt` acceptable for convergence.

    """
    _check_unknown_options(unknown_options)
    tol = xtol
    if brack is None:
        xa, xb, xc, fa, fb, fc, funcalls = bracket(func, args=args)
    elif len(brack) == 2:
        xa, xb, xc, fa, fb, fc, funcalls = bracket(func, xa=brack[0],
                                                   xb=brack[1], args=args)
    elif len(brack) == 3:
        xa, xb, xc = brack
        if (xa > xc):  # swap so xa < xc can be assumed
            xc, xa = xa, xc
        if not ((xa < xb) and (xb < xc)):
            raise ValueError("Not a bracketing interval.")
        fa = func(*((xa,) + args))
        fb = func(*((xb,) + args))
        fc = func(*((xc,) + args))
        if not ((fb < fa) and (fb < fc)):
            raise ValueError("Not a bracketing interval.")
        funcalls = 3
    else:
        raise ValueError("Bracketing interval must be length 2 or 3 sequence.")

    _gR = 0.61803399  # golden ratio conjugate: 2.0/(1.0+sqrt(5.0))
    _gC = 1.0 - _gR
    x3 = xc
    x0 = xa
    if (numpy.abs(xc - xb) > numpy.abs(xb - xa)):
        x1 = xb
        x2 = xb + _gC * (xc - xb)
    else:
        x2 = xb
        x1 = xb - _gC * (xb - xa)
    f1 = func(*((x1,) + args))
    f2 = func(*((x2,) + args))
    funcalls += 2
    nit = 0
    for i in xrange(maxiter):
        if numpy.abs(x3 - x0) <= tol * (numpy.abs(x1) + numpy.abs(x2)):
            break
        if (f2 < f1):
            x0 = x1
            x1 = x2
            x2 = _gR * x1 + _gC * x3
            f1 = f2
            f2 = func(*((x2,) + args))
        else:
            x3 = x2
            x2 = x1
            x1 = _gR * x2 + _gC * x0
            f2 = f1
            f1 = func(*((x1,) + args))
        funcalls += 1
        nit += 1
    if (f1 < f2):
        xmin = x1
        fval = f1
    else:
        xmin = x2
        fval = f2

    return OptimizeResult(fun=fval, nfev=funcalls, x=xmin, nit=nit,
                          success=nit < maxiter)
