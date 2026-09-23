def test_count_nonzero_str():
    x = np.array(list("Hello world"))
    d = da.from_array(x, chunks=(4,))

    x_c = np.count_nonzero(x)
    d_c = da.count_nonzero(d)

    assert x_c == d_c.compute()
