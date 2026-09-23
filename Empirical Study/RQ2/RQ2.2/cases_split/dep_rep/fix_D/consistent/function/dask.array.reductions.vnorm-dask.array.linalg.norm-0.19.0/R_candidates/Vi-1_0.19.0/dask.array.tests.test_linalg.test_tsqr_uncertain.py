@pytest.mark.parametrize('m_min,n_max,chunks,vary_rows,vary_cols,error_type', [
    (10, 5, (10, 5), True, False, None),   # single block tall
    (10, 5, (10, 5), False, True, None),   # single block tall
    (10, 5, (10, 5), True, True, None),    # single block tall
    (40, 5, (10, 5), True, False, None),   # multiple blocks tall
    (40, 5, (10, 5), False, True, None),   # multiple blocks tall
    (40, 5, (10, 5), True, True, None),    # multiple blocks tall
    (300, 10, (40, 10), True, False, None),  # tall-skinny regular thin layers; recursion_depth=2
    (300, 10, (30, 10), True, False, None),  # tall-skinny regular thin layers; recursion_depth=3
    (300, 10, (20, 10), True, False, None),  # tall-skinny regular thin layers; recursion_depth=4
    (300, 10, (40, 10), False, True, None),  # tall-skinny regular thin layers; recursion_depth=2
    (300, 10, (30, 10), False, True, None),  # tall-skinny regular thin layers; recursion_depth=3
    (300, 10, (20, 10), False, True, None),  # tall-skinny regular thin layers; recursion_depth=4
    (300, 10, (40, 10), True, True, None),  # tall-skinny regular thin layers; recursion_depth=2
    (300, 10, (30, 10), True, True, None),  # tall-skinny regular thin layers; recursion_depth=3
    (300, 10, (20, 10), True, True, None),  # tall-skinny regular thin layers; recursion_depth=4
])
def test_tsqr_uncertain(m_min, n_max, chunks, vary_rows, vary_cols, error_type):
    mat = np.random.rand(m_min * 2, n_max)
    m, n = m_min * 2, n_max
    mat[0:m_min, 0] += 1
    _c0 = mat[:, 0]
    _r0 = mat[0, :]
    c0 = da.from_array(_c0, chunks=m_min, name='c')
    r0 = da.from_array(_r0, chunks=n_max, name='r')
    data = da.from_array(mat, chunks=chunks, name='A')
    if vary_rows:
        data = data[c0 > 0.5, :]
        mat = mat[_c0 > 0.5, :]
        m = mat.shape[0]
    if vary_cols:
        data = data[:, r0 > 0.5]
        mat = mat[:, _r0 > 0.5]
        n = mat.shape[1]

    # qr
    m_q = m
    n_q = min(m, n)
    m_r = n_q
    n_r = n

    # svd
    m_u = m
    n_u = min(m, n)
    n_s = n_q
    m_vh = n_q
    n_vh = n
    d_vh = max(m_vh, n_vh)  # full matrix returned

    if error_type is None:
        # test QR
        q, r = tsqr(data)
        q = q.compute()  # because uncertainty
        r = r.compute()
        assert_eq((m_q, n_q), q.shape)  # shape check
        assert_eq((m_r, n_r), r.shape)  # shape check
        assert_eq(mat, np.dot(q, r))  # accuracy check
        assert_eq(np.eye(n_q, n_q), np.dot(q.T, q))  # q must be orthonormal
        assert_eq(r, np.triu(r))  # r must be upper triangular

        # test SVD
        u, s, vh = tsqr(data, compute_svd=True)
        u = u.compute()  # because uncertainty
        s = s.compute()
        vh = vh.compute()
        s_exact = np.linalg.svd(mat)[1]
        assert_eq(s, s_exact)  # s must contain the singular values
        assert_eq((m_u, n_u), u.shape)  # shape check
        assert_eq((n_s,), s.shape)  # shape check
        assert_eq((d_vh, d_vh), vh.shape)  # shape check
        assert_eq(np.eye(n_u, n_u), np.dot(u.T, u))  # u must be orthonormal
        assert_eq(np.eye(d_vh, d_vh), np.dot(vh, vh.T))  # vh must be orthonormal
        assert_eq(mat, np.dot(np.dot(u, np.diag(s)), vh[:n_q]))  # accuracy check
    else:
        with pytest.raises(error_type):
            q, r = tsqr(data)
        with pytest.raises(error_type):
            u, s, vh = tsqr(data, compute_svd=True)
