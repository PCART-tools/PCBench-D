def test_hadamard():
    m, n, p = symbols('m, n, p', integer=True)
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)
    X = MatrixSymbol('X', m, m)
    I = Identity(m)

    raises(TypeError, lambda: hadamard_product())
    assert hadamard_product(A) == A
    assert isinstance(hadamard_product(A, B), HadamardProduct)
    assert hadamard_product(A, B).doit() == hadamard_product(A, B)
    assert hadamard_product(X, I) == HadamardProduct(I, X)
    assert isinstance(hadamard_product(X, I), HadamardProduct)

    a = MatrixSymbol("a", k, 1)
    expr = MatAdd(ZeroMatrix(k, 1), OneMatrix(k, 1))
    expr = HadamardProduct(expr, a)
    assert expr.doit() == a

    raises(ValueError, lambda: HadamardProduct())
