def test_tsqr_zero_height_chunks():
    m_q = 10
    n_q = 5
    m_r = 5
    n_r = 5

    # certainty
    mat = np.random.rand(10, 5)
    x = da.from_array(mat, chunks=((4, 0, 1, 0, 5), (5,)))
    q, r = da.linalg.qr(x)
    assert_eq((m_q, n_q), q.shape)  # shape check
    assert_eq((m_r, n_r), r.shape)  # shape check
    assert_eq(mat, da.dot(q, r))  # accuracy check
    assert_eq(np.eye(n_q, n_q), da.dot(q.T, q))  # q must be orthonormal
    assert_eq(r, da.triu(r.rechunk(r.shape[0])))  # r must be upper triangular

    # uncertainty
    mat2 = np.vstack([mat, -np.ones((10, 5))])
    v2 = mat2[:, 0]
    x2 = da.from_array(mat2, chunks=5)
    c = da.from_array(v2, chunks=5)
    x = x2[c >= 0, :]  # remove the ones added above to yield mat
    q, r = da.linalg.qr(x)
    q = q.compute()  # because uncertainty
    r = r.compute()
    assert_eq((m_q, n_q), q.shape)  # shape check
    assert_eq((m_r, n_r), r.shape)  # shape check
    assert_eq(mat, np.dot(q, r))  # accuracy check
    assert_eq(np.eye(n_q, n_q), np.dot(q.T, q))  # q must be orthonormal
    assert_eq(r, np.triu(r))  # r must be upper triangular
