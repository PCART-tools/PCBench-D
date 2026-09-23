def test_take_sorted():
    chunks, dsk = take('y', 'x', [(20, 20, 20, 20)], [1, 3, 5, 47], axis=0)
    expected = {('y', 0): (getitem, ('x', 0), ([1, 3, 5],)),
                ('y', 1): (getitem, ('x', 2), ([7],))}
    assert dsk == expected
    assert chunks == ((3, 1),)

    chunks, dsk = take('y', 'x', [(20, 20, 20, 20), (20, 20)], [1, 3, 5, 37], axis=1)
    expected = merge(dict((('y', i, 0), (getitem, ('x', i, 0),
                                         (slice(None, None, None), [1, 3, 5])))
                          for i in range(4)),
                     dict((('y', i, 1), (getitem, ('x', i, 1),
                                         (slice(None, None, None), [17])))
                          for i in range(4)))
    assert dsk == expected
    assert chunks == ((20, 20, 20, 20), (3, 1))
