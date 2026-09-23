def test_slice_list_then_None():
    x = da.zeros(shape=(5, 5), chunks=(3, 3))
    y = x[[2, 1]][None]

    assert_eq(y, np.zeros((1, 2, 5)))
