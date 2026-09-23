def test_slicing_with_newaxis():
    result, chunks = slice_array('y', 'x', ([5, 5], [5, 5]),
                            (slice(0, 3), None, slice(None, None, None)))

    expected = {
        ('y', 0, 0, 0): (getitem,
                          ('x', 0, 0),
                          (slice(0, 3, 1), None, slice(None, None, None))),
        ('y', 0, 0, 1): (getitem,
                          ('x', 0, 1),
                          (slice(0, 3, 1), None, slice(None, None, None)))
      }

    assert expected == result
    assert chunks == ((3,), (1,), (5, 5))
