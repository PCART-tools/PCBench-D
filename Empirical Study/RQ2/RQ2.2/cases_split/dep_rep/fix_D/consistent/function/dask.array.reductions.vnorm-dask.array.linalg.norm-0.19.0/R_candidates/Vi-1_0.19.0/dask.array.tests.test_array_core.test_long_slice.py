def test_long_slice():
    x = np.arange(10000)
    d = da.from_array(x, chunks=1)

    assert_eq(d[8000:8200], x[8000:8200])
