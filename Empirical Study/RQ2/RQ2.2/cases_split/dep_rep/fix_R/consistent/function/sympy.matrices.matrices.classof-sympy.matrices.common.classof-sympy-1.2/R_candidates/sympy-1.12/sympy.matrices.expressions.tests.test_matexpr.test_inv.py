def test_inv():
    B = MatrixSymbol('B', 3, 3)
    assert B.inv() == B**-1

    # https://github.com/sympy/sympy/issues/19162
    X = MatrixSymbol('X', 1, 1).as_explicit()
    assert X.inv() == Matrix([[1/X[0, 0]]])

    X = MatrixSymbol('X', 2, 2).as_explicit()
    detX = X[0, 0]*X[1, 1] - X[0, 1]*X[1, 0]
    invX = Matrix([[ X[1, 1], -X[0, 1]],
                   [-X[1, 0],  X[0, 0]]]) / detX
    assert X.inv() == invX
