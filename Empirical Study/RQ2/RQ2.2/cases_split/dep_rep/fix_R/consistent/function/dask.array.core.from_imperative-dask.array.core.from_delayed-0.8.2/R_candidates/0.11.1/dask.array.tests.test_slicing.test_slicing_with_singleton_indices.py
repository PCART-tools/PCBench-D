def test_slicing_with_singleton_indices():
    result, chunks = slice_array('y', 'x', ([5, 5], [5, 5]),
                                    (slice(0, 5), 8))

    expected = {('y', 0): (getitem, ('x', 0, 1), (slice(None, None, None), 3))}

    assert expected == result
