def test_legacy_det():
    # Minimal support for legacy keys for 'method' in det()
    # Partially copied from test_determinant()

    M = Matrix(( ( 3, -2,  0, 5),
                 (-2,  1, -2, 2),
                 ( 0, -2,  5, 0),
                 ( 5,  0,  3, 4) ))

    assert M.det(method="bareis") == -289
    assert M.det(method="det_lu") == -289
    assert M.det(method="det_LU") == -289

    M = Matrix(( (3, 2, 0, 0, 0),
                 (0, 3, 2, 0, 0),
                 (0, 0, 3, 2, 0),
                 (0, 0, 0, 3, 2),
                 (2, 0, 0, 0, 3) ))

    assert M.det(method="bareis") == 275
    assert M.det(method="det_lu") == 275
    assert M.det(method="Bareis") == 275

    M = Matrix(( (1, 0,  1,  2, 12),
                 (2, 0,  1,  1,  4),
                 (2, 1,  1, -1,  3),
                 (3, 2, -1,  1,  8),
                 (1, 1,  1,  0,  6) ))

    assert M.det(method="bareis") == -55
    assert M.det(method="det_lu") == -55
    assert M.det(method="BAREISS") == -55

    M = Matrix(( ( 3,  0,  0, 0),
                 (-2,  1,  0, 0),
                 ( 0, -2,  5, 0),
                 ( 5,  0,  3, 4) ))

    assert M.det(method="bareiss") == 60
    assert M.det(method="berkowitz") == 60
    assert M.det(method="lu") == 60

    M = Matrix(( ( 1,  0,  0,  0),
                 ( 5,  0,  0,  0),
                 ( 9, 10, 11, 0),
                 (13, 14, 15, 16) ))

    assert M.det(method="bareiss") == 0
    assert M.det(method="berkowitz") == 0
    assert M.det(method="lu") == 0

    M = Matrix(( (3, 2, 0, 0, 0),
                 (0, 3, 2, 0, 0),
                 (0, 0, 3, 2, 0),
                 (0, 0, 0, 3, 2),
                 (0, 0, 0, 0, 3) ))

    assert M.det(method="bareiss") == 243
    assert M.det(method="berkowitz") == 243
    assert M.det(method="lu") == 243

    M = Matrix(( (-5,  2,  3,  4,  5),
                 ( 1, -4,  3,  4,  5),
                 ( 1,  2, -3,  4,  5),
                 ( 1,  2,  3, -2,  5),
                 ( 1,  2,  3,  4, -1) ))

    assert M.det(method="bareis") == 11664
    assert M.det(method="det_lu") == 11664
    assert M.det(method="BERKOWITZ") == 11664

    M = Matrix(( ( 2,  7, -1, 3, 2),
                 ( 0,  0,  1, 0, 1),
                 (-2,  0,  7, 0, 2),
                 (-3, -2,  4, 5, 3),
                 ( 1,  0,  0, 0, 1) ))

    assert M.det(method="bareis") == 123
    assert M.det(method="det_lu") == 123
    assert M.det(method="LU") == 123
