def test_evaluate():
    assert MatMul(C, C, evaluate=True) == MatMul(C, C).doit()
