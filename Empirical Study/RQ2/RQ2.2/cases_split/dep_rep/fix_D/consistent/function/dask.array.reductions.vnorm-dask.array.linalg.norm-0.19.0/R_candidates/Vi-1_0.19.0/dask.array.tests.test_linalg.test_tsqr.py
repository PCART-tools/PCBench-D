@pytest.mark.parametrize('m,n,chunks,error_type', [
    (20, 10, 10, None),        # tall-skinny regular blocks
    (20, 10, (3, 10), None),   # tall-skinny regular fat layers
    (20, 10, ((8, 4, 8), 10), None),   # tall-skinny irregular fat layers
    (40, 10, ((15, 5, 5, 8, 7), (10)), None),  # tall-skinny non-uniform chunks (why?)
    (128, 2, (16, 2), None),    # tall-skinny regular thin layers; recursion_depth=1
    (129, 2, (16, 2), None),    # tall-skinny regular thin layers; recursion_depth=2 --> 17x2
    (130, 2, (16, 2), None),    # tall-skinny regular thin layers; recursion_depth=2 --> 18x2 next
    (131, 2, (16, 2), None),    # tall-skinny regular thin layers; recursion_depth=2 --> 18x2 next
    (300, 10, (40, 10), None),  # tall-skinny regular thin layers; recursion_depth=2
    (300, 10, (30, 10), None),  # tall-skinny regular thin layers; recursion_depth=3
    (300, 10, (20, 10), None),  # tall-skinny regular thin layers; recursion_depth=4
    (10, 5, 10, None),         # single block tall
    (5, 10, 10, None),         # single block short
    (10, 10, 10, None),        # single block square
    (10, 40, (10, 10), ValueError),  # short-fat regular blocks
    (10, 40, (10, 15), ValueError),  # short-fat irregular blocks
    (10, 40, ((10), (15, 5, 5, 8, 7)), ValueError),  # short-fat non-uniform chunks (why?)
    (20, 20, 10, ValueError),  # 2x2 regular blocks
])
def test_tsqr(m, n, chunks, error_type):
    mat = np.random.rand(m, n)
    data = da.from_array(mat, chunks=chunks, name='A')

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
        assert_eq((m_q, n_q), q.shape)  # shape check
        assert_eq((m_r, n_r), r.shape)  # shape check
        assert_eq(mat, da.dot(q, r))  # accuracy check
        assert_eq(np.eye(n_q, n_q), da.dot(q.T, q))  # q must be orthonormal
        assert_eq(r, da.triu(r.rechunk(r.shape[0])))  # r must be upper triangular

        # test SVD
        u, s, vh = tsqr(data, compute_svd=True)
        s_exact = np.linalg.svd(mat)[1]
        assert_eq(s, s_exact)  # s must contain the singular values
        assert_eq((m_u, n_u), u.shape)  # shape check
        assert_eq((n_s,), s.shape)  # shape check
        assert_eq((d_vh, d_vh), vh.shape)  # shape check
        assert_eq(np.eye(n_u, n_u), da.dot(u.T, u))  # u must be orthonormal
        assert_eq(np.eye(d_vh, d_vh), da.dot(vh, vh.T))  # vh must be orthonormal
        assert_eq(mat, da.dot(da.dot(u, da.diag(s)), vh[:n_q]))  # accuracy check
    else:
        with pytest.raises(error_type):
            q, r = tsqr(data)
        with pytest.raises(error_type):
            u, s, vh = tsqr(data, compute_svd=True)
