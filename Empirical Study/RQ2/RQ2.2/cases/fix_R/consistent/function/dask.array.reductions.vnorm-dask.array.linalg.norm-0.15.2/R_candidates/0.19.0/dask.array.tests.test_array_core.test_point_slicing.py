def test_point_slicing():
    x = np.arange(56).reshape((7, 8))
    d = da.from_array(x, chunks=(3, 4))

    result = d.vindex[[1, 2, 5, 5], [3, 1, 6, 1]]
    assert_eq(result, x[[1, 2, 5, 5], [3, 1, 6, 1]])

    result = d.vindex[[0, 1, 6, 0], [0, 1, 0, 7]]
    assert_eq(result, x[[0, 1, 6, 0], [0, 1, 0, 7]])
    assert same_keys(result, d.vindex[[0, 1, 6, 0], [0, 1, 0, 7]])
