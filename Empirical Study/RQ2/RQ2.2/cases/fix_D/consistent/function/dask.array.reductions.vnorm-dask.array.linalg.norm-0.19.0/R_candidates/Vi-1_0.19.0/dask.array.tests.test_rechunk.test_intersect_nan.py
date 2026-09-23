def test_intersect_nan():
    old_chunks = ((float('nan'), float('nan')), (8,))
    new_chunks = ((float('nan'), float('nan')), (4, 4))

    result = list(intersect_chunks(old_chunks, new_chunks))
    expected = [
        (((0, slice(0, None, None)), (0, slice(0, 4, None))),),
        (((0, slice(0, None, None)), (0, slice(4, 8, None))),),
        (((1, slice(0, None, None)), (0, slice(0, 4, None))),),
        (((1, slice(0, None, None)), (0, slice(4, 8, None))),)
    ]
    assert result == expected
