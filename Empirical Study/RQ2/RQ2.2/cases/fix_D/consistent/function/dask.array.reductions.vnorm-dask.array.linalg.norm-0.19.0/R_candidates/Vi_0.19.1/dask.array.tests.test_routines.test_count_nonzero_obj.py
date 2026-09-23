def test_count_nonzero_obj():
    x = np.random.randint(10, size=(15, 16)).astype(object)
    d = da.from_array(x, chunks=(4, 5))

    x_c = np.count_nonzero(x)
    d_c = da.count_nonzero(d)

    if d_c.shape == tuple():
        assert x_c == d_c.compute()
    else:
        assert_eq(x_c, d_c)
