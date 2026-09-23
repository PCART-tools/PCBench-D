@pytest.mark.parametrize(('shape', 'chunk'), [(20, 10), (30, 6)])
def test_solve_sym_pos(shape, chunk):
    np.random.seed(1)

    A = _get_symmat(shape)
    dA = da.from_array(A, (chunk, chunk))

    # vector
    b = np.random.random_integers(1, 10, shape)
    db = da.from_array(b, (chunk, chunk))

    res = da.linalg.solve(dA, db, sym_pos=True)
    assert_eq(res, scipy.linalg.solve(A, b, sym_pos=True))
    assert_eq(dA.dot(res), b.astype(float))

    # tall-and-skinny matrix
    b = np.random.random_integers(1, 10, (shape, 5))
    db = da.from_array(b, (chunk, 5))

    res = da.linalg.solve(dA, db, sym_pos=True)
    assert_eq(res, scipy.linalg.solve(A, b, sym_pos=True))
    assert_eq(dA.dot(res), b.astype(float))

    # matrix
    b = np.random.random_integers(1, 10, (shape, shape))
    db = da.from_array(b, (chunk, chunk))

    res = da.linalg.solve(dA, db, sym_pos=True)
    assert_eq(res, scipy.linalg.solve(A, b, sym_pos=True))
    assert_eq(dA.dot(res), b.astype(float))
