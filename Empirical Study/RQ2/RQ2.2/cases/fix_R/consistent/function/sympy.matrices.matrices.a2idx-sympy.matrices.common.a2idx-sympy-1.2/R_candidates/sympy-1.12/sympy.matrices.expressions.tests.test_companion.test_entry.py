def test_entry():
    c0, c1, c2 = symbols('c0:3')
    x = Symbol('x')
    A = CompanionMatrix(Poly([1, c2, c1, c0], x))
    assert A[0, 0] == 0
    assert A[1, 0] == 1
    assert A[1, 1] == 0
    assert A[2, 1] == 1
    assert A[0, 2] == -c0
    assert A[1, 2] == -c1
    assert A[2, 2] == -c2
