def test_trace():
    assert SparseMatrix(((1, 2), (3, 4))).trace() == 5
    assert SparseMatrix(((0, 0), (0, 4))).trace() == 4
