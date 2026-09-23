def test_division():
    v = Matrix(1, 2, [x, y])
    assert v/z == Matrix(1, 2, [x/z, y/z])
