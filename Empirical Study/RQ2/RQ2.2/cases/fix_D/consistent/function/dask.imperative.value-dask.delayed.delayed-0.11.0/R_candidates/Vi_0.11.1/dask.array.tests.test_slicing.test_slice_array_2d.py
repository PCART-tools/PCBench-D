def test_slice_array_2d():
    #2d slices: x[13::2,10::1]
    expected = {('y', 0, 0): (getitem,
                               ('x', 0, 0),
                               (slice(13, 20, 2), slice(10, 20, 1))),
                 ('y', 0, 1): (getitem,
                               ('x', 0, 1),
                               (slice(13, 20, 2), slice(None, None, None))),
                 ('y', 0, 2): (getitem,
                               ('x', 0, 2),
                               (slice(13, 20, 2), slice(None, None, None)))}

    result, chunks = slice_array('y', 'x', [[20], [20, 20, 5]],
                        [slice(13, None, 2), slice(10, None, 1)])

    assert expected == result

    #2d slices with one dimension: x[5,10::1]
    expected = {('y', 0): (getitem,
                               ('x', 0, 0),
                               (5, slice(10, 20, 1))),
                 ('y', 1): (getitem,
                               ('x', 0, 1),
                               (5, slice(None, None, None))),
                 ('y', 2): (getitem,
                               ('x', 0, 2),
                               (5, slice(None, None, None)))}

    result, chunks = slice_array('y', 'x', ([20], [20, 20, 5]),
                        [5, slice(10, None, 1)])

    assert expected == result
