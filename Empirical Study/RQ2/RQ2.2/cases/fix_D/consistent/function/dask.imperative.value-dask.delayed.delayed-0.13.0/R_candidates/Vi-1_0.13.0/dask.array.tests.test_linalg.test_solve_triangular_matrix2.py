@pytest.mark.parametrize(('shape', 'chunk'), [(20, 10), (50, 10), (50, 20)])
def test_solve_triangular_matrix2(shape, chunk):
    np.random.seed(1)

    A = np.random.random_integers(1, 10, (shape, shape))
    b = np.random.random_integers(1, 10, (shape, shape))

    # upper
    Au = np.triu(A)
    dAu = da.from_array(Au, (chunk, chunk))
    db = da.from_array(b, (chunk, chunk))
    res = da.linalg.solve_triangular(dAu, db)
    assert_eq(res, scipy.linalg.solve_triangular(Au, b))
    assert_eq(dAu.dot(res), b.astype(float))

    # lower
    Al = np.tril(A)
    dAl = da.from_array(Al, (chunk, chunk))
    db = da.from_array(b, (chunk, chunk))
    res = da.linalg.solve_triangular(dAl, db, lower=True)
    assert_eq(res, scipy.linalg.solve_triangular(Al, b, lower=True))
    assert_eq(dAl.dot(res), b.astype(float))
