def test_hermite_normal():
    m = Matrix([[2, 7, 17, 29, 41], [3, 11, 19, 31, 43], [5, 13, 23, 37, 47]])
    hnf = Matrix([[1, 0, 0], [0, 2, 1], [0, 0, 1]])
    assert hermite_normal_form(m) == hnf

    tr_hnf = Matrix([[37, 0, 19], [222, -6, 113], [48, 0, 25], [0, 2, 1], [0, 0, 1]])
    assert hermite_normal_form(m.transpose()) == tr_hnf

    m = Matrix([[8, 28, 68, 116, 164], [3, 11, 19, 31, 43], [5, 13, 23, 37, 47]])
    hnf = Matrix([[4, 0, 0], [0, 2, 1], [0, 0, 1]])
    assert hermite_normal_form(m) == hnf
    assert hermite_normal_form(m, D=8) == hnf
    assert hermite_normal_form(m, D=ZZ(8)) == hnf
    assert hermite_normal_form(m, D=Integer(8)) == hnf

    m = Matrix([[10, 8, 6, 30, 2], [45, 36, 27, 18, 9], [5, 4, 3, 2, 1]])
    hnf = Matrix([[26, 2], [0, 9], [0, 1]])
    assert hermite_normal_form(m) == hnf

    m = Matrix([[2, 7], [0, 0], [0, 0]])
    hnf = Matrix([[1], [0], [0]])
    assert hermite_normal_form(m) == hnf
