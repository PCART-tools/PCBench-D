def test_tril_triu_non_square_arrays():
    A = np.random.randint(0, 11, (30, 35))
    dA = da.from_array(A, chunks=(5, 5))
    assert_eq(da.triu(dA), np.triu(A))
    assert_eq(da.tril(dA), np.tril(A))
