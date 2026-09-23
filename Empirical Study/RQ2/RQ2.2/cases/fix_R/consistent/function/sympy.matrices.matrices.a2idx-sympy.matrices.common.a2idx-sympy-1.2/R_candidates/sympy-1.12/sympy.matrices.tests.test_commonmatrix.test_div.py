def test_div():
    n = ArithmeticOnlyMatrix(1, 2, [1, 2])
    assert n/2 == ArithmeticOnlyMatrix(1, 2, [S.Half, S(2)/2])
