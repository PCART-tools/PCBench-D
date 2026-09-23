def _wrap_func(func, x0, fmerit, nfev_list, maxfev, args=()):
    """
    Wrap a function and an initial value so that (i) complex values
    are wrapped to reals, and (ii) value for a merit function
    fmerit(x, f) is computed at the same time, (iii) iteration count
    is maintained and an exception is raised if it is exceeded.

    Parameters
    ----------
    func : callable
        Function to wrap
    x0 : ndarray
        Initial value
    fmerit : callable
        Merit function fmerit(f) for computing merit value from residual.
    nfev_list : list
        List to store number of evaluations in. Should be [0] in the beginning.
    maxfev : int
        Maximum number of evaluations before _NoConvergence is raised.
    args : tuple
        Extra arguments to func

    Returns
    -------
    wrap_func : callable
        Wrapped function, to be called as
        ``F, fp = wrap_func(x0)``
    x0_wrap : ndarray of float
        Wrapped initial value; raveled to 1D and complex
        values mapped to reals.
    x0_shape : tuple
        Shape of the initial value array
    f : float
        Merit function at F
    F : ndarray of float
        Residual at x0_wrap
    is_complex : bool
        Whether complex values were mapped to reals

    """
    x0 = np.asarray(x0)
    x0_shape = x0.shape
    F = np.asarray(func(x0, *args)).ravel()
    is_complex = np.iscomplexobj(x0) or np.iscomplexobj(F)
    x0 = x0.ravel()

    nfev_list[0] = 1

    if is_complex:
        def wrap_func(x):
            if nfev_list[0] >= maxfev:
                raise _NoConvergence()
            nfev_list[0] += 1
            z = _real2complex(x).reshape(x0_shape)
            v = np.asarray(func(z, *args)).ravel()
            F = _complex2real(v)
            f = fmerit(F)
            return f, F

        x0 = _complex2real(x0)
        F = _complex2real(F)
    else:
        def wrap_func(x):
            if nfev_list[0] >= maxfev:
                raise _NoConvergence()
            nfev_list[0] += 1
            x = x.reshape(x0_shape)
            F = np.asarray(func(x, *args)).ravel()
            f = fmerit(F)
            return f, F

    return wrap_func, x0, x0_shape, fmerit(F), F, is_complex
