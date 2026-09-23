def test_inverse():
    assert Inverse(C).args == (C, S.NegativeOne)
    assert Inverse(C).shape == (n, n)
    assert Inverse(A*E).shape == (n, n)
    assert Inverse(E*A).shape == (m, m)
    assert Inverse(C).inverse() == C
    assert Inverse(Inverse(C)).doit() == C
    assert isinstance(Inverse(Inverse(C)), Inverse)

    assert Inverse(*Inverse(E*A).args) == Inverse(E*A)

    assert C.inverse().inverse() == C

    assert C.inverse()*C == Identity(C.rows)

    assert Identity(n).inverse() == Identity(n)
    assert (3*Identity(n)).inverse() == Identity(n)/3

    # Simplifies Muls if possible (i.e. submatrices are square)
    assert (C*D).inverse() == D.I*C.I
    # But still works when not possible
    assert isinstance((A*E).inverse(), Inverse)
    assert Inverse(C*D).doit(inv_expand=False) == Inverse(C*D)

    assert Inverse(eye(3)).doit() == eye(3)
    assert Inverse(eye(3)).doit(deep=False) == eye(3)

    assert OneMatrix(1, 1).I == Identity(1)
    assert isinstance(OneMatrix(n, n).I, Inverse)
