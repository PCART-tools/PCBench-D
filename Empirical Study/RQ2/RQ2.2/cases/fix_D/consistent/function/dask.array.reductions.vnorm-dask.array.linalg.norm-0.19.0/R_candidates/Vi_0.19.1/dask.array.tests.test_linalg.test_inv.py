@pytest.mark.parametrize(('shape', 'chunk'), [(20, 10), (50, 10)])
def test_inv(shape, chunk):
    np.random.seed(1)

    A = np.random.randint(1, 10, (shape, shape))
    dA = da.from_array(A, (chunk, chunk))

    res = da.linalg.inv(dA)
    assert_eq(res, scipy.linalg.inv(A))
    assert_eq(dA.dot(res), np.eye(shape, dtype=float))
