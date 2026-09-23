def test_doit():
    a = OperationsOnlyMatrix([[Add(x, x, evaluate=False)]])
    assert a[0] != 2*x
    assert a.doit() == Matrix([[2*x]])
