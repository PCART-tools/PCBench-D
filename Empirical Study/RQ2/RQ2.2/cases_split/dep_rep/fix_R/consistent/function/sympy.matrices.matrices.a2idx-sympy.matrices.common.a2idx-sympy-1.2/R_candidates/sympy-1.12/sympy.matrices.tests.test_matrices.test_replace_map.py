def test_replace_map():
    F, G = symbols('F, G', cls=Function)
    with warns_deprecated_sympy():
        K = Matrix(2, 2, [(G(0), {F(0): G(0)}), (G(1), {F(1): G(1)}),
                          (G(1), {F(1): G(1)}), (G(2), {F(2): G(2)})])
    M = Matrix(2, 2, lambda i, j: F(i+j))
    with warns(SymPyDeprecationWarning, test_stacklevel=False):
        N = M.replace(F, G, True)
    assert N == K
