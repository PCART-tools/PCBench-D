def test_combine_powers():
    assert combine_powers(MatMul(D, Inverse(D), D, evaluate=False)) == \
                 MatMul(Identity(n), D, evaluate=False)
    assert combine_powers(MatMul(B.T, Inverse(E*A), E, A, B, evaluate=False)) == \
        MatMul(B.T, Identity(m), B, evaluate=False)
    assert combine_powers(MatMul(A, E, Inverse(A*E), D, evaluate=False)) == \
        MatMul(Identity(n), D, evaluate=False)
