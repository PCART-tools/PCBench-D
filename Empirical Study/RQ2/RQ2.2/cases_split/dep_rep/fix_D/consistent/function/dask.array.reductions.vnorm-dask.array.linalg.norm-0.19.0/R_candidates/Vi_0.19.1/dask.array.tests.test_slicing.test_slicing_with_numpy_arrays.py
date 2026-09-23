def test_slicing_with_numpy_arrays():
    a, bd1 = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)),
                         (np.array([1, 2, 9]), slice(None, None, None)))
    b, bd2 = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)),
                         (np.array([1, 2, 9]), slice(None, None, None)))

    assert bd1 == bd2
    np.testing.assert_equal(a, b)

    i = [False, True, True, False, False,
         False, False, False, False, True]
    index = (i, slice(None, None, None))
    index = normalize_index(index, (10, 10))
    c, bd3 = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)), index)
    assert bd1 == bd3
    np.testing.assert_equal(a, c)
