def _check_lu_result(p, l, u, A):
    assert np.allclose(p.dot(l).dot(u), A)

    # check triangulars
    assert np.allclose(l, np.tril(l.compute()))
    assert np.allclose(u, np.triu(u.compute()))
