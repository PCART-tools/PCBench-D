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
    (10, 40, (10, 10), None),  # short-fat regular blocks
    (10, 40, (10, 15), None),  # short-fat irregular blocks
    (10, 40, ((10), (15, 5, 5, 8, 7)), None),  # short-fat non-uniform chunks (why?)
    (20, 20, 10, NotImplementedError),  # 2x2 regular blocks
])
def test_qr(m, n, chunks, error_type):
    mat = np.random.rand(m, n)
    data = da.from_array(mat, chunks=chunks, name='A')
    m_q = m
    n_q = min(m, n)
    m_r = n_q
    n_r = n
    m_qtq = n_q

    if error_type is None:
        q, r = qr(data)
        assert_eq((m_q, n_q), q.shape)  # shape check
        assert_eq((m_r, n_r), r.shape)  # shape check
        assert_eq(mat, da.dot(q, r))  # accuracy check
        assert_eq(np.eye(m_qtq, m_qtq), da.dot(q.T, q))  # q must be orthonormal
        assert_eq(r, da.triu(r.rechunk(r.shape[0])))  # r must be upper triangular
    else:
        with pytest.raises(error_type):
            q, r = qr(data)
