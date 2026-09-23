def test_power():
    raises(NonSquareMatrixError, lambda: Matrix((1, 2))**2)

    A = ArithmeticOnlyMatrix([[2, 3], [4, 5]])
    assert (A**5)[:] == (6140, 8097, 10796, 14237)
    A = ArithmeticOnlyMatrix([[2, 1, 3], [4, 2, 4], [6, 12, 1]])
    assert (A**3)[:] == (290, 262, 251, 448, 440, 368, 702, 954, 433)
    assert A**0 == eye(3)
    assert A**1 == A
    assert (ArithmeticOnlyMatrix([[2]]) ** 100)[0, 0] == 2**100
    assert ArithmeticOnlyMatrix([[1, 2], [3, 4]])**Integer(2) == ArithmeticOnlyMatrix([[7, 10], [15, 22]])
    A = Matrix([[1,2],[4,5]])
    assert A.pow(20, method='cayley') == A.pow(20, method='multiply')
