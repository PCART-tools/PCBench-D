def test_jordan_form():
    m = Matrix(3, 2, [-3, 1, -3, 20, 3, 10])
    raises(NonSquareMatrixError, lambda: m.jordan_form())

    # the next two tests test the cases where the old
    # algorithm failed due to the fact that the block structure can
    # *NOT* be determined  from algebraic and geometric multiplicity alone
    # This can be seen most easily when one lets compute the J.c.f. of a matrix that
    # is in J.c.f already.
    m = Matrix(4, 4, [2, 1, 0, 0,
                    0, 2, 1, 0,
                    0, 0, 2, 0,
                    0, 0, 0, 2
    ])
    P, J = m.jordan_form()
    assert m == J

    m = Matrix(4, 4, [2, 1, 0, 0,
                    0, 2, 0, 0,
                    0, 0, 2, 1,
                    0, 0, 0, 2
    ])
    P, J = m.jordan_form()
    assert m == J

    A = Matrix([[ 2,  4,  1,  0],
                [-4,  2,  0,  1],
                [ 0,  0,  2,  4],
                [ 0,  0, -4,  2]])
    P, J = A.jordan_form()
    assert simplify(P*J*P.inv()) == A

    assert Matrix(1, 1, [1]).jordan_form() == (Matrix([1]), Matrix([1]))
    assert Matrix(1, 1, [1]).jordan_form(calc_transform=False) == Matrix([1])

    # If we have eigenvalues in CRootOf form, raise errors
    m = Matrix([[3, 0, 0, 0, -3], [0, -3, -3, 0, 3], [0, 3, 0, 3, 0], [0, 0, 3, 0, 3], [3, 0, 0, 3, 0]])
    raises(MatrixError, lambda: m.jordan_form())

    # make sure that if the input has floats, the output does too
    m = Matrix([
        [                0.6875, 0.125 + 0.1875*sqrt(3)],
        [0.125 + 0.1875*sqrt(3),                 0.3125]])
    P, J = m.jordan_form()
    assert all(isinstance(x, Float) or x == 0 for x in P)
    assert all(isinstance(x, Float) or x == 0 for x in J)
