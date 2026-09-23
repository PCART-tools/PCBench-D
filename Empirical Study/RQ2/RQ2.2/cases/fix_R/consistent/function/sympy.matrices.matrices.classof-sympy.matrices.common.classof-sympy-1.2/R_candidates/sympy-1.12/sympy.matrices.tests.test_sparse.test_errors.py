def test_errors():
    raises(ValueError, lambda: SparseMatrix(1.4, 2, lambda i, j: 0))
    raises(TypeError, lambda: SparseMatrix([1, 2, 3], [1, 2]))
    raises(ValueError, lambda: SparseMatrix([[1, 2], [3, 4]])[(1, 2, 3)])
    raises(IndexError, lambda: SparseMatrix([[1, 2], [3, 4]])[5])
    raises(ValueError, lambda: SparseMatrix([[1, 2], [3, 4]])[1, 2, 3])
    raises(TypeError,
        lambda: SparseMatrix([[1, 2], [3, 4]]).copyin_list([0, 1], set()))
    raises(
        IndexError, lambda: SparseMatrix([[1, 2], [3, 4]])[1, 2])
    raises(TypeError, lambda: SparseMatrix([1, 2, 3]).cross(1))
    raises(IndexError, lambda: SparseMatrix(1, 2, [1, 2])[3])
    raises(ShapeError,
        lambda: SparseMatrix(1, 2, [1, 2]) + SparseMatrix(2, 1, [2, 1]))
