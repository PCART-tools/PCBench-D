def eigenhproblem_standard(desc, dim, dtype,
                           overwrite, lower, turbo,
                           eigvals):
    """Solve a standard eigenvalue problem."""
    if iscomplex(empty(1, dtype=dtype)):
        a = _complex_symrand(dim, dtype)
    else:
        a = symrand(dim).astype(dtype)

    if overwrite:
        a_c = a.copy()
    else:
        a_c = a
    w, z = eigh(a, overwrite_a=overwrite, lower=lower, eigvals=eigvals)
    assert_dtype_equal(z.dtype, dtype)
    w = w.astype(dtype)
    diag_ = diag(dot(z.T.conj(), dot(a_c, z))).real
    assert_array_almost_equal(diag_, w, DIGITS[dtype])
