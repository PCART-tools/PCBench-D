def test_simplify():
    n = Symbol('n')
    f = Function('f')

    M = OperationsOnlyMatrix([[            1/x + 1/y,                 (x + x*y) / x  ],
                [ (f(x) + y*f(x))/f(x), 2 * (1/n - cos(n * pi)/n) / pi ]])
    assert M.simplify() == Matrix([[ (x + y)/(x * y),                        1 + y ],
                        [           1 + y, 2*((1 - 1*cos(pi*n))/(pi*n)) ]])
    eq = (1 + x)**2
    M = OperationsOnlyMatrix([[eq]])
    assert M.simplify() == Matrix([[eq]])
    assert M.simplify(ratio=oo) == Matrix([[eq.simplify(ratio=oo)]])

    # https://github.com/sympy/sympy/issues/19353
    m = Matrix([[30, 2], [3, 4]])
    assert (1/(m.trace())).simplify() == Rational(1, 34)
