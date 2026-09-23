def test_add():
    assert SparseMatrix(((1, 0), (0, 1))) + SparseMatrix(((0, 1), (1, 0))) == \
        SparseMatrix(((1, 1), (1, 1)))
    a = SparseMatrix(100, 100, lambda i, j: int(j != 0 and i % j == 0))
    b = SparseMatrix(100, 100, lambda i, j: int(i != 0 and j % i == 0))
    assert (len(a.todok()) + len(b.todok()) - len((a + b).todok()) > 0)
