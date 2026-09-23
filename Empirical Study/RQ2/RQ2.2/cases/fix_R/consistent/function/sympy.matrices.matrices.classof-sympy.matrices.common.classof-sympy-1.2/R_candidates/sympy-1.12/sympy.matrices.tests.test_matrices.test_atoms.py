def test_atoms():
    m = Matrix([[1, 2], [x, 1 - 1/x]])
    assert m.atoms() == {S.One,S(2),S.NegativeOne, x}
    assert m.atoms(Symbol) == {x}
