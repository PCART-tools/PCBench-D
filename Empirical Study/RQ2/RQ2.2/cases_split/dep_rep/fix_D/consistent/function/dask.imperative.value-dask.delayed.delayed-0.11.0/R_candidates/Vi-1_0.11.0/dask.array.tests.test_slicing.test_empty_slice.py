def test_empty_slice():
    x = da.ones((5, 5), chunks=(2, 2), dtype='i4')
    y = x[:0]

    assert eq(y, np.ones((5, 5), dtype='i4')[:0])
