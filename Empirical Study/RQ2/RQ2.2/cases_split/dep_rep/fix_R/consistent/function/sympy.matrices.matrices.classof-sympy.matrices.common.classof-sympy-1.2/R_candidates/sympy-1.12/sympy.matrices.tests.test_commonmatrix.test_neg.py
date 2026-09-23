def test_neg():
    n = ArithmeticOnlyMatrix(1, 2, [1, 2])
    assert -n == ArithmeticOnlyMatrix(1, 2, [-1, -2])
