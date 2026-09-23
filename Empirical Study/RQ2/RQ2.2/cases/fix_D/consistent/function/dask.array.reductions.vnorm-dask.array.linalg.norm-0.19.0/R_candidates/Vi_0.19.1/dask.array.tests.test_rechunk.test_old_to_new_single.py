def test_old_to_new_single():
    old = ((float('nan'), float('nan')), (8,))
    new = ((float('nan'), float('nan')), (4, 4))
    result = _old_to_new(old, new)

    expected = [[[(0, slice(0, None, None))], [(1, slice(0, None, None))]],
                [[(0, slice(0, 4, None))], [(0, slice(4, 8, None))]]]

    assert result == expected
