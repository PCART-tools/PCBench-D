def test_hermitian():
    x = Symbol('x')
    a = SparseMatrix([[0, I], [-I, 0]])
    assert a.is_hermitian
    a = SparseMatrix([[1, I], [-I, 1]])
    assert a.is_hermitian
    a[0, 0] = 2*I
    assert a.is_hermitian is False
    a[0, 0] = x
    assert a.is_hermitian is None
    a[0, 1] = a[1, 0]*I
    assert a.is_hermitian is False
