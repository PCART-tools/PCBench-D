def test_doit():
    assert MatMul(C, 2, D).args == (C, 2, D)
    assert MatMul(C, 2, D).doit().args == (2, C, D)
    assert MatMul(C, Transpose(D*C)).args == (C, Transpose(D*C))
    assert MatMul(C, Transpose(D*C)).doit(deep=True).args == (C, C.T, D.T)
