def find_best_blas_type(arrays=(), dtype=None):
    """Find best-matching BLAS/LAPACK type.

    Arrays are used to determine the optimal prefix of BLAS routines.

    Parameters
    ----------
    arrays : sequence of ndarrays, optional
        Arrays can be given to determine optimal prefix of BLAS
        routines. If not given, double-precision routines will be
        used, otherwise the most generic type in arrays will be used.
    dtype : str or dtype, optional
        Data-type specifier. Not used if `arrays` is non-empty.

    Returns
    -------
    prefix : str
        BLAS/LAPACK prefix character.
    dtype : dtype
        Inferred Numpy data type.
    prefer_fortran : bool
        Whether to prefer Fortran order routines over C order.

    Examples
    --------
    >>> import scipy.linalg.blas as bla
    >>> a = np.random.rand(10,15)
    >>> b = np.asfortranarray(a)  # Change the memory layout order
    >>> bla.find_best_blas_type((a,))
    ('d', dtype('float64'), False)
    >>> bla.find_best_blas_type((a*1j,))
    ('z', dtype('complex128'), False)
    >>> bla.find_best_blas_type((b,))
    ('d', dtype('float64'), True)

    """
    dtype = _np.dtype(dtype)
    prefer_fortran = False

    if arrays:
        # use the most generic type in arrays
        dtypes = [ar.dtype for ar in arrays]
        dtype = _np.find_common_type(dtypes, ())
        try:
            index = dtypes.index(dtype)
        except ValueError:
            index = 0
        if arrays[index].flags['FORTRAN']:
            # prefer Fortran for leading array with column major order
            prefer_fortran = True

    prefix = _type_conv.get(dtype.char, 'd')
    if dtype.char == 'G':
        # complex256 -> complex128 (i.e., C long double -> C double)
        dtype = _np.dtype('D')
    elif dtype.char not in 'fdFD':
        dtype = _np.dtype('d')

    return prefix, dtype, prefer_fortran
