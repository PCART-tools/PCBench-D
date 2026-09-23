@pytest.mark.slow
def test_svd_compressed():
    m, n = 2000, 250
    r = 10
    np.random.seed(4321)
    mat1 = np.random.randn(m, r)
    mat2 = np.random.randn(r, n)
    mat = mat1.dot(mat2)
    data = da.from_array(mat, chunks=(500, 50))

    u, s, vt = svd_compressed(data, r, seed=4321, n_power_iter=2)

    usvt = da.dot(u, da.dot(da.diag(s), vt))

    tol = 0.2
    assert_eq(da.linalg.norm(usvt),
              np.linalg.norm(mat),
              rtol=tol, atol=tol)  # average accuracy check

    u = u[:, :r]
    s = s[:r]
    vt = vt[:r, :]

    s_exact = np.linalg.svd(mat)[1]
    s_exact = s_exact[:r]

    assert_eq(np.eye(r, r), da.dot(u.T, u))  # u must be orthonormal
    assert_eq(np.eye(r, r), da.dot(vt, vt.T))  # v must be orthonormal
    assert_eq(s, s_exact)  # s must contain the singular values
