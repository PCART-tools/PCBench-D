def test_zeros():
    assert list(SpecialOnlyMatrix.zeros(2, 2)) == [0, 0, 0, 0]
    assert list(SpecialOnlyMatrix.zeros(2)) == [0, 0, 0, 0]
    assert SpecialOnlyMatrix.zeros(2, 3) == Matrix([[0, 0, 0], [0, 0, 0]])
    assert type(SpecialOnlyMatrix.zeros(2)) == SpecialOnlyMatrix
    assert type(SpecialOnlyMatrix.zeros(2, cls=Matrix)) == Matrix
