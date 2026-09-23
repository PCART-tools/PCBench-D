def test_slicing_chunks():
    result, chunks = slice_array('y', 'x', ([5, 5], [5, 5]),
                                    (1, [2, 0, 3]))
    assert chunks == ((3,),)

    result, chunks = slice_array('y', 'x', ([5, 5], [5, 5]),
                                    (slice(0, 7), [2, 0, 3]))
    assert chunks == ((5, 2), (3,))

    result, chunks = slice_array('y', 'x', ([5, 5], [5, 5]),
                                    (slice(0, 7), 1))
    assert chunks == ((5, 2),)
