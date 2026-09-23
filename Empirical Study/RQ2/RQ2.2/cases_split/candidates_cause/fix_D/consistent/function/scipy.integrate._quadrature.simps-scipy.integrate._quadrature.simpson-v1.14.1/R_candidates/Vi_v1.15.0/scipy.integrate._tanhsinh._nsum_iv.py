def _nsum_iv(f, a, b, step, args, log, maxterms, tolerances):
    # Input validation and standardization

    xp = array_namespace(a, b)

    message = '`f` must be callable.'
    if not callable(f):
        raise ValueError(message)

    message = 'All elements of `a`, `b`, and `step` must be real numbers.'
    a, b, step = xp.broadcast_arrays(xp.asarray(a), xp.asarray(b), xp.asarray(step))
    dtype = xp.result_type(a.dtype, b.dtype, step.dtype)
    if not xp.isdtype(dtype, 'numeric') or xp.isdtype(dtype, 'complex floating'):
        raise ValueError(message)

    valid_b = b >= a  # NaNs will be False
    valid_step = xp.isfinite(step) & (step > 0)
    valid_abstep = valid_b & valid_step

    message = '`log` must be True or False.'
    if log not in {True, False}:
        raise ValueError(message)

    tolerances = {} if tolerances is None else tolerances

    atol = tolerances.get('atol', None)
    if atol is None:
        atol = -xp.inf if log else 0

    rtol = tolerances.get('rtol', None)
    rtol_temp = rtol if rtol is not None else 0.

    # using NumPy for convenience here; these are just floats, not arrays
    params = np.asarray([atol, rtol_temp, 0.])
    message = "`atol` and `rtol` must be real numbers."
    if not np.issubdtype(params.dtype, np.floating):
        raise ValueError(message)

    if log:
        message = '`atol`, `rtol` may not be positive infinity or NaN.'
        if np.any(np.isposinf(params) | np.isnan(params)):
            raise ValueError(message)
    else:
        message = '`atol`, and `rtol` must be non-negative and finite.'
        if np.any((params < 0) | (~np.isfinite(params))):
            raise ValueError(message)
    atol = params[0]
    rtol = rtol if rtol is None else params[1]

    maxterms_int = int(maxterms)
    if maxterms_int != maxterms or maxterms < 0:
        message = "`maxterms` must be a non-negative integer."
        raise ValueError(message)

    if not np.iterable(args):
        args = (args,)

    return f, a, b, step, valid_abstep, args, log, maxterms_int, atol, rtol, xp
