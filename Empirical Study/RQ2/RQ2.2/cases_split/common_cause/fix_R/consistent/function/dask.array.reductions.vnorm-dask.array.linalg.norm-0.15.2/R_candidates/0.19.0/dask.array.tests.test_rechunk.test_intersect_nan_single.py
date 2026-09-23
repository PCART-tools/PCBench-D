def test_intersect_nan_single():
    old_chunks = ((float('nan'),), (10,))
    new_chunks = ((float('nan'),), (5, 5))

    result = list(intersect_chunks(old_chunks, new_chunks))
    expected = [(((0, slice(0, None, None)), (0, slice(0, 5, None))),),
                (((0, slice(0, None, None)), (0, slice(5, 10, None))),)]
    assert result == expected
