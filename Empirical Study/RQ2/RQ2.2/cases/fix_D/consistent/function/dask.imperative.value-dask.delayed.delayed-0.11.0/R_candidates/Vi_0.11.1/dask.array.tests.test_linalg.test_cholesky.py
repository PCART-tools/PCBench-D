@pytest.mark.parametrize(('shape', 'chunk'), [(20, 10), (12, 3), (30, 3), (30, 6)])
def test_cholesky(shape, chunk):

    A = _get_symmat(shape)
    dA = da.from_array(A, (chunk, chunk))
    assert_eq(da.linalg.cholesky(dA), scipy.linalg.cholesky(A))
    assert_eq(da.linalg.cholesky(dA, lower=True), scipy.linalg.cholesky(A, lower=True))
