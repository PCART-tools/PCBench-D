def test_creation():
    raises(ValueError, lambda: Matrix(5, 5, range(20)))
    raises(ValueError, lambda: Matrix(5, -1, []))
    raises(IndexError, lambda: Matrix((1, 2))[2])
    with raises(IndexError):
        Matrix((1, 2))[3] = 5

    assert Matrix() == Matrix([]) == Matrix([[]]) == Matrix(0, 0, [])
    # anything used to be allowed in a matrix
    with warns_deprecated_sympy():
        assert Matrix([[[1], (2,)]]).tolist() == [[[1], (2,)]]
    with warns_deprecated_sympy():
        assert Matrix([[[1], (2,)]]).T.tolist() == [[[1]], [(2,)]]
    M = Matrix([[0]])
    with warns_deprecated_sympy():
        M[0, 0] = S.EmptySet

    a = Matrix([[x, 0], [0, 0]])
    m = a
    assert m.cols == m.rows
    assert m.cols == 2
    assert m[:] == [x, 0, 0, 0]

    b = Matrix(2, 2, [x, 0, 0, 0])
    m = b
    assert m.cols == m.rows
    assert m.cols == 2
    assert m[:] == [x, 0, 0, 0]

    assert a == b

    assert Matrix(b) == b

    c23 = Matrix(2, 3, range(1, 7))
    c13 = Matrix(1, 3, range(7, 10))
    c = Matrix([c23, c13])
    assert c.cols == 3
    assert c.rows == 3
    assert c[:] == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    assert Matrix(eye(2)) == eye(2)
    assert ImmutableMatrix(ImmutableMatrix(eye(2))) == ImmutableMatrix(eye(2))
    assert ImmutableMatrix(c) == c.as_immutable()
    assert Matrix(ImmutableMatrix(c)) == ImmutableMatrix(c).as_mutable()

    assert c is not Matrix(c)

    dat = [[ones(3,2), ones(3,3)*2], [ones(2,3)*3, ones(2,2)*4]]
    M = Matrix(dat)
    assert M == Matrix([
        [1, 1, 2, 2, 2],
        [1, 1, 2, 2, 2],
        [1, 1, 2, 2, 2],
        [3, 3, 3, 4, 4],
        [3, 3, 3, 4, 4]])
    assert M.tolist() != dat
    # keep block form if evaluate=False
    assert Matrix(dat, evaluate=False).tolist() == dat
    A = MatrixSymbol("A", 2, 2)
    dat = [ones(2), A]
    assert Matrix(dat) == Matrix([
    [      1,       1],
    [      1,       1],
    [A[0, 0], A[0, 1]],
    [A[1, 0], A[1, 1]]])
    with warns_deprecated_sympy():
        assert Matrix(dat, evaluate=False).tolist() == [[i] for i in dat]

    # 0-dim tolerance
    assert Matrix([ones(2), ones(0)]) == Matrix([ones(2)])
    raises(ValueError, lambda: Matrix([ones(2), ones(0, 3)]))
    raises(ValueError, lambda: Matrix([ones(2), ones(3, 0)]))

    # mix of Matrix and iterable
    M = Matrix([[1, 2], [3, 4]])
    M2 = Matrix([M, (5, 6)])
    assert M2 == Matrix([[1, 2], [3, 4], [5, 6]])
