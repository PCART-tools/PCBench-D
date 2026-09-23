def test_tsqr_svd_regular_blocks():
    m, n = 20, 10
    mat = np.random.rand(m, n)
    data = da.from_array(mat, chunks=(10, n), name='A')

    u, s, vt = tsqr(data, compute_svd=True)
    u = np.array(u)
    s = np.array(s)
    vt = np.array(vt)
    usvt = np.dot(u, np.dot(np.diag(s), vt))

    s_exact = np.linalg.svd(mat)[1]

    assert_eq(mat, usvt)  # accuracy check
    assert_eq(np.eye(n, n), np.dot(u.T, u))  # u must be orthonormal
    assert_eq(np.eye(n, n), np.dot(vt, vt.T))  # v must be orthonormal
    assert_eq(s, s_exact)  # s must contain the singular values
