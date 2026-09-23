def test_is_zero():
    assert PropertiesOnlyMatrix(0, 0, []).is_zero_matrix
    assert PropertiesOnlyMatrix([[0, 0], [0, 0]]).is_zero_matrix
    assert PropertiesOnlyMatrix(zeros(3, 4)).is_zero_matrix
    assert not PropertiesOnlyMatrix(eye(3)).is_zero_matrix
    assert PropertiesOnlyMatrix([[x, 0], [0, 0]]).is_zero_matrix == None
    assert PropertiesOnlyMatrix([[x, 1], [0, 0]]).is_zero_matrix == False
    a = Symbol('a', nonzero=True)
    assert PropertiesOnlyMatrix([[a, 0], [0, 0]]).is_zero_matrix == False
