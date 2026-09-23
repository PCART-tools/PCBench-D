def test_QR():
    A = Matrix([[1, 2], [2, 3]])
    Q, S = A.QRdecomposition()
    R = Rational
    assert Q == Matrix([
        [  5**R(-1, 2),  (R(2)/5)*(R(1)/5)**R(-1, 2)],
        [2*5**R(-1, 2), (-R(1)/5)*(R(1)/5)**R(-1, 2)]])
    assert S == Matrix([[5**R(1, 2), 8*5**R(-1, 2)], [0, (R(1)/5)**R(1, 2)]])
    assert Q*S == A
    assert Q.T * Q == eye(2)

    A = Matrix([[1, 1, 1], [1, 1, 3], [2, 3, 4]])
    Q, R = A.QRdecomposition()
    assert Q.T * Q == eye(Q.cols)
    assert R.is_upper
    assert A == Q*R

    A = Matrix([[12, 0, -51], [6, 0, 167], [-4, 0, 24]])
    Q, R = A.QRdecomposition()
    assert Q.T * Q == eye(Q.cols)
    assert R.is_upper
    assert A == Q*R

    x = Symbol('x')
    A = Matrix([x])
    Q, R = A.QRdecomposition()
    assert Q == Matrix([x / Abs(x)])
    assert R == Matrix([Abs(x)])

    A = Matrix([[x, 0], [0, x]])
    Q, R = A.QRdecomposition()
    assert Q == x / Abs(x) * Matrix([[1, 0], [0, 1]])
    assert R == Abs(x) * Matrix([[1, 0], [0, 1]])
