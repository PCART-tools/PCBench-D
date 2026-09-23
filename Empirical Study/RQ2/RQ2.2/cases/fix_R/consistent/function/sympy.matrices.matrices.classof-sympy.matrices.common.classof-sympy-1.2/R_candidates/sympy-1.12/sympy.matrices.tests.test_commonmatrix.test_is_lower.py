def test_is_lower():
    a = PropertiesOnlyMatrix([[1, 2, 3]])
    assert a.is_lower is False
    a = PropertiesOnlyMatrix([[1], [2], [3]])
    assert a.is_lower is True
