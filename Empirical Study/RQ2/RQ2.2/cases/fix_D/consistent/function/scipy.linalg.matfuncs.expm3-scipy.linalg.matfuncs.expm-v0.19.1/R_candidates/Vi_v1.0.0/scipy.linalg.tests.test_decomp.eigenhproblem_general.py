def eigenhproblem_general(desc, dim, dtype,
                          overwrite, lower, turbo,
                          eigenvalues):
    """Solve a generalized eigenvalue problem."""
    if iscomplex(empty(1, dtype=dtype)):
        a = _complex_symrand(dim, dtype)
        b = _complex_symrand(dim, dtype)+diag([2.1]*dim).astype(dtype)
    else:
        a = symrand(dim).astype(dtype)
        b = symrand(dim).astype(dtype)+diag([2.1]*dim).astype(dtype)

    if overwrite:
        a_c, b_c = a.copy(), b.copy()
    else:
        a_c, b_c = a, b

    w, z = eigh(a, b, overwrite_a=overwrite, lower=lower,
                overwrite_b=overwrite, turbo=turbo, eigvals=eigenvalues)
    assert_dtype_equal(z.dtype, dtype)
    w = w.astype(dtype)
    diag1_ = diag(dot(z.T.conj(), dot(a_c, z))).real
    assert_array_almost_equal(diag1_, w, DIGITS[dtype])
    diag2_ = diag(dot(z.T.conj(), dot(b_c, z))).real
    assert_array_almost_equal(diag2_, ones(diag2_.shape[0]), DIGITS[dtype])
