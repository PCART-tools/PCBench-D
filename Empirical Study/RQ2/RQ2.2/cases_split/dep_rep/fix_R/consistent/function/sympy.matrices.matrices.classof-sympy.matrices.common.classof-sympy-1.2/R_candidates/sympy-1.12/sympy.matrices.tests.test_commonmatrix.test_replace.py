def test_replace():
    F, G = symbols('F, G', cls=Function)
    K = OperationsOnlyMatrix(2, 2, lambda i, j: G(i+j))
    M = OperationsOnlyMatrix(2, 2, lambda i, j: F(i+j))
    N = M.replace(F, G)
    assert N == K
