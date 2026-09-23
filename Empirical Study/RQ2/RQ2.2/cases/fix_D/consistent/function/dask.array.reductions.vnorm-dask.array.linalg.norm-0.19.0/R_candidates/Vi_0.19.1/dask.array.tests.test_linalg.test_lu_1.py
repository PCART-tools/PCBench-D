def test_lu_1():
    A1 = np.array([[7, 3, -1, 2], [3, 8, 1, -4],
                  [-1, 1, 4, -1], [2, -4, -1, 6] ])

    A2 = np.array([[7,  0,  0,  0,  0,  0],
                   [0,  8,  0,  0,  0,  0],
                   [0,  0,  4,  0,  0,  0],
                   [0,  0,  0,  6,  0,  0],
                   [0,  0,  0,  0,  3,  0],
                   [0,  0,  0,  0,  0,  5]])
    # without shuffle
    for A, chunk in zip([A1, A2], [2, 2]):
        dA = da.from_array(A, chunks=(chunk, chunk))
        p, l, u = scipy.linalg.lu(A)
        dp, dl, du = da.linalg.lu(dA)
        assert_eq(p, dp)
        assert_eq(l, dl)
        assert_eq(u, du)
        _check_lu_result(dp, dl, du, A)

    A3 = np.array([[ 7,  3,  2,  1,  4,  1],
                   [ 7, 11,  5,  2,  5,  2],
                   [21, 25, 16, 10, 16,  5],
                   [21, 41, 18, 13, 16, 11],
                   [14, 46, 23, 24, 21, 22],
                   [ 0, 56, 29, 17, 14, 8]])

    # with shuffle
    for A, chunk in zip([A3], [2]):
        dA = da.from_array(A, chunks=(chunk, chunk))
        p, l, u = scipy.linalg.lu(A)
        dp, dl, du = da.linalg.lu(dA)
        _check_lu_result(dp, dl, du, A)
