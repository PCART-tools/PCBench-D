def test_slice_lists():
    y, chunks = slice_array('y', 'x', ((3, 3, 3, 1), (3, 3, 3, 1)),
                                ([2, 1, 9], slice(None, None, None)))
    assert y == \
        dict((('y', 0, i), (getitem,
                       (np.concatenate,
                        (list,
                         [(getitem,
                           ('x', 0, i),
                           ([1, 2], slice(None, None, None))),
                          (getitem,
                           ('x', 3, i),
                           ([0], slice(None, None, None))),
                           ]),
                        0),
                       ([1, 0, 2], slice(None, None, None))))
                for i in range(4))

    assert chunks == ((3,), (3, 3, 3, 1))
