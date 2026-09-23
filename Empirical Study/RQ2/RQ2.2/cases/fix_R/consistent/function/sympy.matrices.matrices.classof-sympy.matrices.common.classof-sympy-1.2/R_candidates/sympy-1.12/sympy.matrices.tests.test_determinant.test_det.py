def test_det():
    a = Matrix(2, 3, [1, 2, 3, 4, 5, 6])
    raises(NonSquareMatrixError, lambda: a.det())

    z = zeros_Determinant(2)
    ey = eye_Determinant(2)
    assert z.det() == 0
    assert ey.det() == 1

    x = Symbol('x')
    a = Matrix(0, 0, [])
    b = Matrix(1, 1, [5])
    c = Matrix(2, 2, [1, 2, 3, 4])
    d = Matrix(3, 3, [1, 2, 3, 4, 5, 6, 7, 8, 8])
    e = Matrix(4, 4,
        [x, 1, 2, 3, 4, 5, 6, 7, 2, 9, 10, 11, 12, 13, 14, 14])
    from sympy.abc import i, j, k, l, m, n
    f = Matrix(3, 3, [i, l, m, 0, j, n, 0, 0, k])
    g = Matrix(3, 3, [i, 0, 0, l, j, 0, m, n, k])
    h = Matrix(3, 3, [x**3, 0, 0, i, x**-1, 0, j, k, x**-2])
    # the method keyword for `det` doesn't kick in until 4x4 matrices,
    # so there is no need to test all methods on smaller ones

    assert a.det() == 1
    assert b.det() == 5
    assert c.det() == -2
    assert d.det() == 3
    assert e.det() == 4*x - 24
    assert e.det(method="domain-ge") == 4*x - 24
    assert e.det(method='bareiss') == 4*x - 24
    assert e.det(method='berkowitz') == 4*x - 24
    assert f.det() == i*j*k
    assert g.det() == i*j*k
    assert h.det() == 1
    raises(ValueError, lambda: e.det(iszerofunc="test"))
