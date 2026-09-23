def test_values():
    assert set(PropertiesOnlyMatrix(2, 2, [0, 1, 2, 3]
        ).values()) == {1, 2, 3}
    x = Symbol('x', real=True)
    assert set(PropertiesOnlyMatrix(2, 2, [x, 0, 0, 1]
        ).values()) == {x, 1}
