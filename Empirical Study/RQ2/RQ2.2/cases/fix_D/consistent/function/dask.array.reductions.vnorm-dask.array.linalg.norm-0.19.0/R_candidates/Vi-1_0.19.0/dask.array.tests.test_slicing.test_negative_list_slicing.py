def test_negative_list_slicing():
    x = np.arange(5)
    dx = da.from_array(x, chunks=2)
    assert_eq(dx[[0, -5]], x[[0, -5]])
    assert_eq(dx[[4, -1]], x[[4, -1]])
