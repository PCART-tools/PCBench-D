def test_has():
    A = PropertiesOnlyMatrix(((x, y), (2, 3)))
    assert A.has(x)
    assert not A.has(z)
    assert A.has(Symbol)

    A = PropertiesOnlyMatrix(((2, y), (2, 3)))
    assert not A.has(x)
