def test_limit():
    x, y = symbols('x y')
    m = CalculusOnlyMatrix(2, 1, [1/x, y])
    assert m.limit(x, 5) == Matrix(2, 1, [Rational(1, 5), y])
