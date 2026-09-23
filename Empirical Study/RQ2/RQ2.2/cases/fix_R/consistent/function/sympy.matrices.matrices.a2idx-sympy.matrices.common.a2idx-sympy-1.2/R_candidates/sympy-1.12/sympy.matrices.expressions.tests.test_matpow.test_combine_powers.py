def test_combine_powers():
    assert (C ** 1) ** 1 == C
    assert (C ** 2) ** 3 == MatPow(C, 6)
    assert (C ** -2) ** -3 == MatPow(C, 6)
    assert (C ** -1) ** -1 == C
    assert (((C ** 2) ** 3) ** 4) ** 5 == MatPow(C, 120)
    assert (C ** n) ** n == C ** (n ** 2)
