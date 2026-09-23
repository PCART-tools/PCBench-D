def test_MatPow():
    A = MatrixSymbol('A', n, n)

    AA = MatPow(A, 2)
    assert AA.exp == 2
    assert AA.base == A
    assert (A**n).exp == n

    assert A**0 == Identity(n)
    assert A**1 == A
    assert A**2 == AA
    assert A**-1 == Inverse(A)
    assert (A**-1)**-1 == A
    assert (A**2)**3 == A**6
    assert A**S.Half == sqrt(A)
    assert A**Rational(1, 3) == cbrt(A)
    raises(NonSquareMatrixError, lambda: MatrixSymbol('B', 3, 2)**2)
