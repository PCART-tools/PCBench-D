def eig_banded(a_band, lower=False, eigvals_only=False, overwrite_a_band=False,
               select='a', select_range=None, max_ev=0, check_finite=True):
    """
    Solve real symmetric or complex hermitian band matrix eigenvalue problem.

    Find eigenvalues w and optionally right eigenvectors v of a::

        a v[:,i] = w[i] v[:,i]
        v.H v    = identity

    The matrix a is stored in a_band either in lower diagonal or upper
    diagonal ordered form:

        a_band[u + i - j, j] == a[i,j]        (if upper form; i <= j)
        a_band[    i - j, j] == a[i,j]        (if lower form; i >= j)

    where u is the number of bands above the diagonal.

    Example of a_band (shape of a is (6,6), u=2)::

        upper form:
        *   *   a02 a13 a24 a35
        *   a01 a12 a23 a34 a45
        a00 a11 a22 a33 a44 a55

        lower form:
        a00 a11 a22 a33 a44 a55
        a10 a21 a32 a43 a54 *
        a20 a31 a42 a53 *   *

    Cells marked with * are not used.

    Parameters
    ----------
    a_band : (u+1, M) array_like
        The bands of the M by M matrix a.
    lower : bool, optional
        Is the matrix in the lower form. (Default is upper form)
    eigvals_only : bool, optional
        Compute only the eigenvalues and no eigenvectors.
        (Default: calculate also eigenvectors)
    overwrite_a_band : bool, optional
        Discard data in a_band (may enhance performance)
    select : {'a', 'v', 'i'}, optional
        Which eigenvalues to calculate

        ======  ========================================
        select  calculated
        ======  ========================================
        'a'     All eigenvalues
        'v'     Eigenvalues in the interval (min, max]
        'i'     Eigenvalues with indices min <= i <= max
        ======  ========================================
    select_range : (min, max), optional
        Range of selected eigenvalues
    max_ev : int, optional
        For select=='v', maximum number of eigenvalues expected.
        For other values of select, has no meaning.

        In doubt, leave this parameter untouched.

    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    w : (M,) ndarray
        The eigenvalues, in ascending order, each repeated according to its
        multiplicity.
    v : (M, M) float or complex ndarray
        The normalized eigenvector corresponding to the eigenvalue w[i] is
        the column v[:,i].

    Raises LinAlgError if eigenvalue computation does not converge

    """
    if eigvals_only or overwrite_a_band:
        a1 = _asarray_validated(a_band, check_finite=check_finite)
        overwrite_a_band = overwrite_a_band or (_datacopied(a1, a_band))
    else:
        a1 = array(a_band)
        if issubclass(a1.dtype.type, inexact) and not isfinite(a1).all():
            raise ValueError("array must not contain infs or NaNs")
        overwrite_a_band = 1

    if len(a1.shape) != 2:
        raise ValueError('expected two-dimensional array')
    if select.lower() not in [0, 1, 2, 'a', 'v', 'i', 'all', 'value', 'index']:
        raise ValueError('invalid argument for select')
    if select.lower() in [0, 'a', 'all']:
        if a1.dtype.char in 'GFD':
            bevd, = get_lapack_funcs(('hbevd',), (a1,))
            # FIXME: implement this somewhen, for now go with builtin values
            # FIXME: calc optimal lwork by calling ?hbevd(lwork=-1)
            #        or by using calc_lwork.f ???
            # lwork = calc_lwork.hbevd(bevd.typecode, a1.shape[0], lower)
            internal_name = 'hbevd'
        else:  # a1.dtype.char in 'fd':
            bevd, = get_lapack_funcs(('sbevd',), (a1,))
            # FIXME: implement this somewhen, for now go with builtin values
            #         see above
            # lwork = calc_lwork.sbevd(bevd.typecode, a1.shape[0], lower)
            internal_name = 'sbevd'
        w,v,info = bevd(a1, compute_v=not eigvals_only,
                        lower=lower,
                        overwrite_ab=overwrite_a_band)
    if select.lower() in [1, 2, 'i', 'v', 'index', 'value']:
        # calculate certain range only
        if select.lower() in [2, 'i', 'index']:
            select = 2
            vl, vu, il, iu = 0.0, 0.0, min(select_range), max(select_range)
            if min(il, iu) < 0 or max(il, iu) >= a1.shape[1]:
                raise ValueError('select_range out of bounds')
            max_ev = iu - il + 1
        else:  # 1, 'v', 'value'
            select = 1
            vl, vu, il, iu = min(select_range), max(select_range), 0, 0
            if max_ev == 0:
                max_ev = a_band.shape[1]
        if eigvals_only:
            max_ev = 1
        # calculate optimal abstol for dsbevx (see manpage)
        if a1.dtype.char in 'fF':  # single precision
            lamch, = get_lapack_funcs(('lamch',), (array(0, dtype='f'),))
        else:
            lamch, = get_lapack_funcs(('lamch',), (array(0, dtype='d'),))
        abstol = 2 * lamch('s')
        if a1.dtype.char in 'GFD':
            bevx, = get_lapack_funcs(('hbevx',), (a1,))
            internal_name = 'hbevx'
        else:  # a1.dtype.char in 'gfd'
            bevx, = get_lapack_funcs(('sbevx',), (a1,))
            internal_name = 'sbevx'
        # il+1, iu+1: translate python indexing (0 ... N-1) into Fortran
        # indexing (1 ... N)
        w, v, m, ifail, info = bevx(a1, vl, vu, il+1, iu+1,
                                    compute_v=not eigvals_only,
                                    mmax=max_ev,
                                    range=select, lower=lower,
                                    overwrite_ab=overwrite_a_band,
                                    abstol=abstol)
        # crop off w and v
        w = w[:m]
        if not eigvals_only:
            v = v[:, :m]
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal %s'
                                                    % (-info, internal_name))
    if info > 0:
        raise LinAlgError("eig algorithm did not converge")

    if eigvals_only:
        return w
    return w, v
