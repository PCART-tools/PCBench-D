def test_shape_error():
    A = MatrixSymbol('A', 2, 3)
    B = MatrixSymbol('B', 3, 3)
    raises(ShapeError, lambda: HadamardProduct(A, B))
    raises(ShapeError, lambda: HadamardPower(A, B))
    A = MatrixSymbol('A', 3, 2)
    raises(ShapeError, lambda: HadamardProduct(A, B))
    raises(ShapeError, lambda: HadamardPower(A, B))
