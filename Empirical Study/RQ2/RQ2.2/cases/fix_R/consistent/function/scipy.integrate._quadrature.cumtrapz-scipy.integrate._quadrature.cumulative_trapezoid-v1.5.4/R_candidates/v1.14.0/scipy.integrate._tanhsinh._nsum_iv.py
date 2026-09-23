def _nsum_iv(f, a, b, step, args, log, maxterms, atol, rtol):
    # Input validation and standardization

    message = '`f` must be callable.'
    if not callable(f):
        raise ValueError(message)

    message = 'All elements of `a`, `b`, and `step` must be real numbers.'
    a, b, step = np.broadcast_arrays(a, b, step)
    dtype = np.result_type(a.dtype, b.dtype, step.dtype)
    if not np.issubdtype(dtype, np.number) or np.issubdtype(dtype, np.complexfloating):
        raise ValueError(message)

    valid_a = np.isfinite(a)
    valid_b = b >= a  # NaNs will be False
    valid_step = np.isfinite(step) & (step > 0)
    valid_abstep = valid_a & valid_b & valid_step

    message = '`log` must be True or False.'
    if log not in {True, False}:
        raise ValueError(message)

    if atol is None:
        atol = -np.inf if log else 0

    rtol_temp = rtol if rtol is not None else 0.

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

    return f, a, b, step, valid_abstep, args, log, maxterms_int, atol, rtol
