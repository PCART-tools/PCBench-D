def test_allclose():
    n_a = np.array([0, np.nan, 1, 1.5])
    n_b = np.array([1e-9, np.nan, 1, 2])

    d_a = da.from_array(n_a, chunks=(2,))
    d_b = da.from_array(n_b, chunks=(2,))

    n_r = np.allclose(n_a, n_b, equal_nan=True)
    d_r = da.allclose(d_a, d_b, equal_nan=True)

    assert_eq(np.array(n_r)[()], d_r)
