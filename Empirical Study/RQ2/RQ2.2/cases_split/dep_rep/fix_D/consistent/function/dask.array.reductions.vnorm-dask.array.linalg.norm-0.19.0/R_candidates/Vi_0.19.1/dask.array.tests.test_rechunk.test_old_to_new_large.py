def test_old_to_new_large():
    old = (tuple([float('nan')] * 4), (10,))
    new = (tuple([float('nan')] * 4), (5, 5))

    result = _old_to_new(old, new)
    expected = [[[(0, slice(0, None, None))],
                [(1, slice(0, None, None))],
                [(2, slice(0, None, None))],
                [(3, slice(0, None, None))]],
                [[(0, slice(0, 5, None))], [(0, slice(5, 10, None))]]]
    assert result == expected
