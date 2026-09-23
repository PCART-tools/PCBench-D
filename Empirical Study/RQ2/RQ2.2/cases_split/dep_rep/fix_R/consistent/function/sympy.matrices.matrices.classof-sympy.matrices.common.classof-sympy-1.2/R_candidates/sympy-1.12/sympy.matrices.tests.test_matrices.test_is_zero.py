def test_is_zero():
    assert Matrix().is_zero_matrix
    assert Matrix([[0, 0], [0, 0]]).is_zero_matrix
    assert zeros(3, 4).is_zero_matrix
    assert not eye(3).is_zero_matrix
    assert Matrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert SparseMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert ImmutableMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert ImmutableSparseMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert Matrix([[x, 1], [0, 0]]).is_zero_matrix == False
    a = Symbol('a', nonzero=True)
    assert Matrix([[a, 0], [0, 0]]).is_zero_matrix == False
