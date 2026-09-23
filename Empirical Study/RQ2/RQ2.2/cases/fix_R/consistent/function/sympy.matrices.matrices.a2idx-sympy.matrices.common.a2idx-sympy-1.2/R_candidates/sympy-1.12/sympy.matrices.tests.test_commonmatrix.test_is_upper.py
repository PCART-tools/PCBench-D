def test_is_upper():
    a = PropertiesOnlyMatrix([[1, 2, 3]])
    assert a.is_upper is True
    a = PropertiesOnlyMatrix([[1], [2], [3]])
    assert a.is_upper is False
