def test_len():
    assert not SparseMatrix()
    assert SparseMatrix() == SparseMatrix([])
    assert SparseMatrix() == SparseMatrix([[]])
