def test_shape():
    m = ShapingOnlyMatrix(1, 2, [0, 0])
    assert m.shape == (1, 2)
