def test_linalg_consistent_names():
    m, n = 20, 10
    mat = np.random.rand(m, n)
    data = da.from_array(mat, chunks=(10, n), name='A')

    q1, r1 = qr(data)
    q2, r2 = qr(data)
    assert same_keys(q1, q2)
    assert same_keys(r1, r2)

    u1, s1, v1 = svd(data)
    u2, s2, v2 = svd(data)
    assert same_keys(u1, u2)
    assert same_keys(s1, s2)
    assert same_keys(v1, v2)
