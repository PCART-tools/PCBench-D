def test_shape_error():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 3, 3)
    raises(ShapeError, lambda: MatMul(A, B))
