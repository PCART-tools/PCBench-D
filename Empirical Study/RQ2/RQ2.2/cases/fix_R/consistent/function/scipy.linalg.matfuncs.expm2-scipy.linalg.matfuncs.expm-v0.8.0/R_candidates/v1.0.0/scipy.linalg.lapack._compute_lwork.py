def _compute_lwork(routine, *args, **kwargs):
    """
    Round floating-point lwork returned by lapack to integer.

    Several LAPACK routines compute optimal values for LWORK, which
    they return in a floating-point variable. However, for large
    values of LWORK, single-precision floating point is not sufficient
    to hold the exact value --- some LAPACK versions (<= 3.5.0 at
    least) truncate the returned integer to single precision and in
    some cases this can be smaller than the required value.

    Examples
    --------
    >>> from scipy.linalg import lapack
    >>> n = 5000
    >>> s_r, s_lw = lapack.get_lapack_funcs(('sysvx', 'sysvx_lwork'))
    >>> lwork = lapack._compute_lwork(s_lw, n)
    >>> lwork
    32000

    """
    wi = routine(*args, **kwargs)
    if len(wi) < 2:
        raise ValueError('')
    info = wi[-1]
    if info != 0:
        raise ValueError("Internal work array size computation failed: "
                         "%d" % (info,))

    lwork = [w.real for w in wi[:-1]]

    dtype = getattr(routine, 'dtype', None)
    if dtype == _np.float32 or dtype == _np.complex64:
        # Single-precision routine -- take next fp value to work
        # around possible truncation in LAPACK code
        lwork = _np.nextafter(lwork, _np.inf, dtype=_np.float32)

    lwork = _np.array(lwork, _np.int64)
    if _np.any(_np.logical_or(lwork < 0, lwork > _np.iinfo(_np.int32).max)):
        raise ValueError("Too large work array required -- computation cannot "
                         "be performed with standard 32-bit LAPACK.")
    lwork = lwork.astype(_np.int32)
    if lwork.size == 1:
        return lwork[0]
    return lwork
