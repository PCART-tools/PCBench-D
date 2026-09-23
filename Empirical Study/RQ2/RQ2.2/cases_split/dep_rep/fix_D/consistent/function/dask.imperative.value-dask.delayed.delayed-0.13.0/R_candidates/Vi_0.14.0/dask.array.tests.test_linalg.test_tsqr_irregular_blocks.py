def test_tsqr_irregular_blocks():
    m, n = 20, 10
    mat = np.random.rand(m, n)
    data = da.from_array(mat, chunks=(3, n), name='A')[1:]
    mat2 = mat[1:, :]

    q, r = tsqr(data)
    q = np.array(q)
    r = np.array(r)

    assert_eq(mat2, np.dot(q, r))  # accuracy check
    assert_eq(np.eye(n, n), np.dot(q.T, q))  # q must be orthonormal
    assert_eq(r, np.triu(r))  # r must be upper triangular
