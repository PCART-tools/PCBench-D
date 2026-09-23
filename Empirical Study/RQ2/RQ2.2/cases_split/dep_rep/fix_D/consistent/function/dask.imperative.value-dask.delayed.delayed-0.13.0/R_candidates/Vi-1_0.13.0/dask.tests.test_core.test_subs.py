def test_subs():
    assert subs((sum, [1, 'x']), 'x', 2) == (sum, [1, 2])
    assert subs((sum, [1, ['x']]), 'x', 2) == (sum, [1, [2]])
