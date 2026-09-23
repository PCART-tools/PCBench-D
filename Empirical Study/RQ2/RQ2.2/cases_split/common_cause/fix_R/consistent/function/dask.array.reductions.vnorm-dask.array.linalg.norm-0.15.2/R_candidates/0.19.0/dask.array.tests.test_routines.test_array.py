def test_array():
    x = np.ones(5, dtype='i4')
    d = da.ones(5, chunks=3, dtype='i4')
    assert_eq(da.array(d, ndmin=3, dtype='i8'),
              np.array(x, ndmin=3, dtype='i8'))

    # regression #1847 this shall not raise an exception.
    x = da.ones((100,3), chunks=10)
    y = da.array(x)
    assert isinstance(y, da.Array)
