def test_as_explicit():
    Z = MatrixSymbol('Z', 2, 3)
    assert Z.as_explicit() == ImmutableMatrix([
        [Z[0, 0], Z[0, 1], Z[0, 2]],
        [Z[1, 0], Z[1, 1], Z[1, 2]],
    ])
    raises(ValueError, lambda: A.as_explicit())
