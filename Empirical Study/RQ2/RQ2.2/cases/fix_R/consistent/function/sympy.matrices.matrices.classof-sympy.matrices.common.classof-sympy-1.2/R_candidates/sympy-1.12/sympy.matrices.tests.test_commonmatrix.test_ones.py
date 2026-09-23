def test_ones():
    assert list(SpecialOnlyMatrix.ones(2, 2)) == [1, 1, 1, 1]
    assert list(SpecialOnlyMatrix.ones(2)) == [1, 1, 1, 1]
    assert SpecialOnlyMatrix.ones(2, 3) == Matrix([[1, 1, 1], [1, 1, 1]])
    assert type(SpecialOnlyMatrix.ones(2)) == SpecialOnlyMatrix
    assert type(SpecialOnlyMatrix.ones(2, cls=Matrix)) == Matrix
