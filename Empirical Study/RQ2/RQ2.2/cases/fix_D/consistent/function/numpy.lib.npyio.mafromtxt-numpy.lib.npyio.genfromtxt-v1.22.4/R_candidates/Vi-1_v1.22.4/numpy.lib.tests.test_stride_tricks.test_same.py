def test_same():
    x = np.arange(10)
    y = np.arange(10)
    bx, by = broadcast_arrays(x, y)
    assert_array_equal(x, bx)
    assert_array_equal(y, by)
