def test_old_to_new():
    old = ((float('nan'),), (10,))
    new = ((float('nan'),), (5, 5))
    result = _old_to_new(old, new)
    expected = [[[(0, slice(0, None, None))]],
                [[(0, slice(0, 5, None))], [(0, slice(5, 10, None))]]]

    assert result == expected
