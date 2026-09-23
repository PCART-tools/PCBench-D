def _make_complex_eigvecs(w, vin, dtype):
    """
    Produce complex-valued eigenvectors from LAPACK DGGEV real-valued output
    """
    # - see LAPACK man page DGGEV at ALPHAI
    v = numpy.array(vin, dtype=dtype)
    m = (w.imag > 0)
    m[:-1] |= (w.imag[1:] < 0)  # workaround for LAPACK bug, cf. ticket #709
    for i in flatnonzero(m):
        v.imag[:, i] = vin[:, i+1]
        conj(v[:, i], v[:, i+1])
    return v
