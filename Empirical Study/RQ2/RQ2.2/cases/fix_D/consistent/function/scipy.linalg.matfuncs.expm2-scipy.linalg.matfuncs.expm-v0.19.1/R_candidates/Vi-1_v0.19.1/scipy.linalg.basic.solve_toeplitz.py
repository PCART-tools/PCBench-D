def solve_toeplitz(c_or_cr, b, check_finite=True):
    """Solve a Toeplitz system using Levinson Recursion

    The Toeplitz matrix has constant diagonals, with c as its first column
    and r as its first row.  If r is not given, ``r == conjugate(c)`` is
    assumed.

    Parameters
    ----------
    c_or_cr : array_like or tuple of (array_like, array_like)
        The vector ``c``, or a tuple of arrays (``c``, ``r``). Whatever the
        actual shape of ``c``, it will be converted to a 1-D array. If not
        supplied, ``r = conjugate(c)`` is assumed; in this case, if c[0] is
        real, the Toeplitz matrix is Hermitian. r[0] is ignored; the first row
        of the Toeplitz matrix is ``[c[0], r[1:]]``.  Whatever the actual shape
        of ``r``, it will be converted to a 1-D array.
    b : (M,) or (M, K) array_like
        Right-hand side in ``T x = b``.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (result entirely NaNs) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, K) ndarray
        The solution to the system ``T x = b``.  Shape of return matches shape
        of `b`.

    Notes
    -----
    The solution is computed using Levinson-Durbin recursion, which is faster
    than generic least-squares methods, but can be less numerically stable.
    """
    # If numerical stability of this algorithm is a problem, a future
    # developer might consider implementing other O(N^2) Toeplitz solvers,
    # such as GKO (http://www.jstor.org/stable/2153371) or Bareiss.
    if isinstance(c_or_cr, tuple):
        c, r = c_or_cr
        c = _asarray_validated(c, check_finite=check_finite).ravel()
        r = _asarray_validated(r, check_finite=check_finite).ravel()
    else:
        c = _asarray_validated(c_or_cr, check_finite=check_finite).ravel()
        r = c.conjugate()

    # Form a 1D array of values to be used in the matrix, containing a reversed
    # copy of r[1:], followed by c.
    vals = np.concatenate((r[-1:0:-1], c))
    if b is None:
        raise ValueError('illegal value, `b` is a required argument')

    b = _asarray_validated(b)
    if vals.shape[0] != (2*b.shape[0] - 1):
        raise ValueError('incompatible dimensions')
    if np.iscomplexobj(vals) or np.iscomplexobj(b):
        vals = np.asarray(vals, dtype=np.complex128, order='c')
        b = np.asarray(b, dtype=np.complex128)
    else:
        vals = np.asarray(vals, dtype=np.double, order='c')
        b = np.asarray(b, dtype=np.double)

    if b.ndim == 1:
        x, _ = levinson(vals, np.ascontiguousarray(b))
    else:
        b_shape = b.shape
        b = b.reshape(b.shape[0], -1)
        x = np.column_stack(
            (levinson(vals, np.ascontiguousarray(b[:, i]))[0])
            for i in range(b.shape[1]))
        x = x.reshape(*b_shape)

    return x
