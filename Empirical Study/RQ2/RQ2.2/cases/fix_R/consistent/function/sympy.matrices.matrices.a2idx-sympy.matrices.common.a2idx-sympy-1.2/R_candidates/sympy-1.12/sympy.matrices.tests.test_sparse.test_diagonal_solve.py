def test_diagonal_solve():
    a, d = symbols('a d')
    u, v, w, x = symbols('u:x')

    A = SparseMatrix([[a, 0], [0, d]])
    B = MutableSparseMatrix([[u, v], [w, x]])
    C = ImmutableSparseMatrix([[u, v], [w, x]])

    sol = Matrix([[u/a, v/a], [w/d, x/d]])
    assert A.diagonal_solve(B) == sol
    assert A.diagonal_solve(C) == sol
