def test_rank():
    m = Matrix([[1, 2], [x, 1 - 1/x]])
    assert m.rank() == 2
    n = Matrix(3, 3, range(1, 10))
    assert n.rank() == 2
    p = zeros(3)
    assert p.rank() == 0
