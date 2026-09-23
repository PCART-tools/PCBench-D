def test_slicing_with_numpy_arrays():
    a, bd1 = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)),
                         ([1, 2, 9], slice(None, None, None)))
    b, bd2 = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)),
                         (np.array([1, 2, 9]), slice(None, None, None)))

    assert bd1 == bd2
    assert a == b

    i = [False, True, True, False, False,
         False, False, False, False, True, False]
    c, bd3 = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)),
                         (i, slice(None, None, None)))
    assert bd1 == bd3
    assert a == c
