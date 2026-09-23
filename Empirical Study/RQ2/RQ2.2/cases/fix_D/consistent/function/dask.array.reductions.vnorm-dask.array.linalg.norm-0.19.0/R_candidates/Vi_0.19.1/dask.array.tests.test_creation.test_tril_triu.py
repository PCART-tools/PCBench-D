def test_tril_triu():
    A = np.random.randn(20, 20)
    for chk in [5, 4]:
        dA = da.from_array(A, (chk, chk))

        assert np.allclose(da.triu(dA).compute(), np.triu(A))
        assert np.allclose(da.tril(dA).compute(), np.tril(A))

        for k in [-25, -20, -19, -15, -14, -9, -8, -6, -5, -1,
                  1, 4, 5, 6, 8, 10, 11, 15, 16, 19, 20, 21]:
            assert np.allclose(da.triu(dA, k).compute(), np.triu(A, k))
            assert np.allclose(da.tril(dA, k).compute(), np.tril(A, k))
