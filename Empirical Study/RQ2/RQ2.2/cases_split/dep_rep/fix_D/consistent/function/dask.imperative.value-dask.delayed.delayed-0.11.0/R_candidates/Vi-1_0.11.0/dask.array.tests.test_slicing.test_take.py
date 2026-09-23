def test_take():
    chunks, dsk = take('y', 'x', [(20, 20, 20, 20)], [5, 1, 47, 3], axis=0)
    expected = {('y', 0):
            (getitem,
              (np.concatenate, (list,
                [(getitem, ('x', 0), ([1, 3, 5],)),
                 (getitem, ('x', 2), ([7],))]),
               0),
             ([2, 0, 3, 1],))}
    assert dsk == expected
    assert chunks == ((4,),)

    chunks, dsk = take('y', 'x', [(20, 20, 20, 20), (20, 20)], [5, 1, 47, 3], axis=0)
    expected = dict((('y', 0, j),
            (getitem,
              (np.concatenate, (list,
                [(getitem, ('x', 0, j), ([1, 3, 5], slice(None, None, None))),
                 (getitem, ('x', 2, j), ([7], slice(None, None, None)))]),
                0),
              ([2, 0, 3, 1], slice(None, None, None))))
            for j in range(2))
    assert dsk == expected
    assert chunks == ((4,), (20, 20))

    chunks, dsk = take('y', 'x', [(20, 20, 20, 20), (20, 20)], [5, 1, 37, 3], axis=1)
    expected = dict((('y', i, 0),
            (getitem,
              (np.concatenate, (list,
                [(getitem, ('x', i, 0), (slice(None, None, None), [1, 3, 5])),
                 (getitem, ('x', i, 1), (slice(None, None, None), [17]))]),
                1),
             (slice(None, None, None), [2, 0, 3, 1])))
           for i in range(4))
    assert dsk == expected
    assert chunks == ((20, 20, 20, 20), (4,))
