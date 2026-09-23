def test_abs():
    m = ArithmeticOnlyMatrix([[1, -2], [x, y]])
    assert abs(m) == ArithmeticOnlyMatrix([[1, 2], [Abs(x), Abs(y)]])
