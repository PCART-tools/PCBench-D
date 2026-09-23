def test_exp():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    expr1 = exp(A)*exp(B)
    expr2 = exp(B)*exp(A)
    assert expr1 != expr2
    assert expr1 - expr2 != 0
    assert not isinstance(expr1, exp)
    assert not isinstance(expr2, exp)
