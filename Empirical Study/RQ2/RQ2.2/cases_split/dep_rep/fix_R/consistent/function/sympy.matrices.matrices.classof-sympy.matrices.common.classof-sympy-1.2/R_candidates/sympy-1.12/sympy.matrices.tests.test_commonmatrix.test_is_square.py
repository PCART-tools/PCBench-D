def test_is_square():
    m = PropertiesOnlyMatrix([[1], [1]])
    m2 = PropertiesOnlyMatrix([[2, 2], [2, 2]])
    assert not m.is_square
    assert m2.is_square
