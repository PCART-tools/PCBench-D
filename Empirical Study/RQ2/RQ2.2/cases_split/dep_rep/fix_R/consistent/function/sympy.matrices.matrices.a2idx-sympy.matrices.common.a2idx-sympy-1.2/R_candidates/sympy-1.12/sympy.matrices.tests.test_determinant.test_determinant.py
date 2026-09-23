def test_determinant():
    M = Matrix()

    assert M.det() == 1
    # Evaluating these directly because they are never reached via M.det()
    assert M._eval_det_bareiss() == 1
    assert M._eval_det_berkowitz() == 1
    assert M._eval_det_lu() == 1

    M = Matrix([ [0] ])

    assert M.det() == 0
    assert M._eval_det_bareiss() == 0
    assert M._eval_det_berkowitz() == 0
    assert M._eval_det_lu() == 0

    M = Matrix([ [5] ])

    assert M.det() == 5
    assert M._eval_det_bareiss() == 5
    assert M._eval_det_berkowitz() == 5
    assert M._eval_det_lu() == 5

    M = Matrix(( (-3,  2),
                 ( 8, -5) ))

    assert M.det(method="domain-ge") == -1
    assert M.det(method="bareiss") == -1
    assert M.det(method="berkowitz") == -1
    assert M.det(method="lu") == -1

    M = Matrix(( (x,   1),
                 (y, 2*y) ))

    assert M.det(method="domain-ge") == 2*x*y - y
    assert M.det(method="bareiss") == 2*x*y - y
    assert M.det(method="berkowitz") == 2*x*y - y
    assert M.det(method="lu") == 2*x*y - y

    M = Matrix(( (1, 1, 1),
                 (1, 2, 3),
                 (1, 3, 6) ))

    assert M.det(method="domain-ge") == 1
    assert M.det(method="bareiss") == 1
    assert M.det(method="berkowitz") == 1
    assert M.det(method="lu") == 1

    M = Matrix(( ( 3, -2,  0, 5),
                 (-2,  1, -2, 2),
                 ( 0, -2,  5, 0),
                 ( 5,  0,  3, 4) ))

    assert M.det(method="domain-ge") == -289
    assert M.det(method="bareiss") == -289
    assert M.det(method="berkowitz") == -289
    assert M.det(method="lu") == -289

    M = Matrix(( ( 1,  2,  3,  4),
                 ( 5,  6,  7,  8),
                 ( 9, 10, 11, 12),
                 (13, 14, 15, 16) ))

    assert M.det(method="domain-ge") == 0
    assert M.det(method="bareiss") == 0
    assert M.det(method="berkowitz") == 0
    assert M.det(method="lu") == 0

    M = Matrix(( (3, 2, 0, 0, 0),
                 (0, 3, 2, 0, 0),
                 (0, 0, 3, 2, 0),
                 (0, 0, 0, 3, 2),
                 (2, 0, 0, 0, 3) ))

    assert M.det(method="domain-ge") == 275
    assert M.det(method="bareiss") == 275
    assert M.det(method="berkowitz") == 275
    assert M.det(method="lu") == 275

    M = Matrix(( ( 3,  0,  0, 0),
                 (-2,  1,  0, 0),
                 ( 0, -2,  5, 0),
                 ( 5,  0,  3, 4) ))

    assert M.det(method="domain-ge") == 60
    assert M.det(method="bareiss") == 60
    assert M.det(method="berkowitz") == 60
    assert M.det(method="lu") == 60

    M = Matrix(( ( 1,  0,  0,  0),
                 ( 5,  0,  0,  0),
                 ( 9, 10, 11, 0),
                 (13, 14, 15, 16) ))

    assert M.det(method="domain-ge") == 0
    assert M.det(method="bareiss") == 0
    assert M.det(method="berkowitz") == 0
    assert M.det(method="lu") == 0

    M = Matrix(( (3, 2, 0, 0, 0),
                 (0, 3, 2, 0, 0),
                 (0, 0, 3, 2, 0),
                 (0, 0, 0, 3, 2),
                 (0, 0, 0, 0, 3) ))

    assert M.det(method="domain-ge") == 243
    assert M.det(method="bareiss") == 243
    assert M.det(method="berkowitz") == 243
    assert M.det(method="lu") == 243

    M = Matrix(( (1, 0,  1,  2, 12),
                 (2, 0,  1,  1,  4),
                 (2, 1,  1, -1,  3),
                 (3, 2, -1,  1,  8),
                 (1, 1,  1,  0,  6) ))

    assert M.det(method="domain-ge") == -55
    assert M.det(method="bareiss") == -55
    assert M.det(method="berkowitz") == -55
    assert M.det(method="lu") == -55

    M = Matrix(( (-5,  2,  3,  4,  5),
                 ( 1, -4,  3,  4,  5),
                 ( 1,  2, -3,  4,  5),
                 ( 1,  2,  3, -2,  5),
                 ( 1,  2,  3,  4, -1) ))

    assert M.det(method="domain-ge") == 11664
    assert M.det(method="bareiss") == 11664
    assert M.det(method="berkowitz") == 11664
    assert M.det(method="lu") == 11664

    M = Matrix(( ( 2,  7, -1, 3, 2),
                 ( 0,  0,  1, 0, 1),
                 (-2,  0,  7, 0, 2),
                 (-3, -2,  4, 5, 3),
                 ( 1,  0,  0, 0, 1) ))

    assert M.det(method="domain-ge") == 123
    assert M.det(method="bareiss") == 123
    assert M.det(method="berkowitz") == 123
    assert M.det(method="lu") == 123

    M = Matrix(( (x, y, z),
                 (1, 0, 0),
                 (y, z, x) ))

    assert M.det(method="domain-ge") == z**2 - x*y
    assert M.det(method="bareiss") == z**2 - x*y
    assert M.det(method="berkowitz") == z**2 - x*y
    assert M.det(method="lu") == z**2 - x*y

    # issue 13835
    a = symbols('a')
    M = lambda n: Matrix([[i + a*j for i in range(n)]
                          for j in range(n)])
    assert M(5).det() == 0
    assert M(6).det() == 0
    assert M(7).det() == 0
