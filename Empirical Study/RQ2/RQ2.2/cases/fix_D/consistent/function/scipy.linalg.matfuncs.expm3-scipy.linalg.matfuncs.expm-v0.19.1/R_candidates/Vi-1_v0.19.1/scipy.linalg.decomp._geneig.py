def _geneig(a1, b1, left, right, overwrite_a, overwrite_b, homogeneous_eigvals):
    ggev, = get_lapack_funcs(('ggev',), (a1, b1))
    cvl, cvr = left, right
    res = ggev(a1, b1, lwork=-1)
    lwork = res[-2][0].real.astype(numpy.int)
    if ggev.typecode in 'cz':
        alpha, beta, vl, vr, work, info = ggev(a1, b1, cvl, cvr, lwork,
                                               overwrite_a, overwrite_b)
        w = _make_eigvals(alpha, beta, homogeneous_eigvals)
    else:
        alphar, alphai, beta, vl, vr, work, info = ggev(a1, b1, cvl, cvr,
                                                        lwork, overwrite_a,
                                                        overwrite_b)
        alpha = alphar + _I * alphai
        w = _make_eigvals(alpha, beta, homogeneous_eigvals)
    if info < 0:
        raise ValueError('illegal value in %d-th argument of internal ggev' %
                         -info)
    if info > 0:
        raise LinAlgError("generalized eig algorithm did not converge "
                          "(info=%d)" % info)

    only_real = numpy.all(w.imag == 0.0)
    if not (ggev.typecode in 'cz' or only_real):
        t = w.dtype.char
        if left:
            vl = _make_complex_eigvecs(w, vl, t)
        if right:
            vr = _make_complex_eigvecs(w, vr, t)

    # the eigenvectors returned by the lapack function are NOT normalized
    for i in xrange(vr.shape[0]):
        if right:
            vr[:, i] /= norm(vr[:, i])
        if left:
            vl[:, i] /= norm(vl[:, i])

    if not (left or right):
        return w
    if left:
        if right:
            return w, vl, vr
        return w, vl
    return w, vr
