def _check_lu_result(p, l, u, A):
    assert np.allclose(p.dot(l).dot(u), A)

    # check triangulars
    assert_eq(l, da.tril(l))
    assert_eq(u, da.triu(u))
