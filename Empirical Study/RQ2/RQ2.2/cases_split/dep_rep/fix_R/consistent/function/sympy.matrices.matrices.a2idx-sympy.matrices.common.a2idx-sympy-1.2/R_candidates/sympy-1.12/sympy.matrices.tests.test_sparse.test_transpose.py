def test_transpose():
    assert SparseMatrix(((1, 2), (3, 4))).transpose() == \
        SparseMatrix(((1, 3), (2, 4)))
