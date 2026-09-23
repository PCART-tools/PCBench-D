def test_as_real_imag():
    m1 = OperationsOnlyMatrix(2, 2, [1, 2, 3, 4])
    m3 = OperationsOnlyMatrix(2, 2,
        [1 + S.ImaginaryUnit, 2 + 2*S.ImaginaryUnit,
        3 + 3*S.ImaginaryUnit, 4 + 4*S.ImaginaryUnit])

    a, b = m3.as_real_imag()
    assert a == m1
    assert b == m1
