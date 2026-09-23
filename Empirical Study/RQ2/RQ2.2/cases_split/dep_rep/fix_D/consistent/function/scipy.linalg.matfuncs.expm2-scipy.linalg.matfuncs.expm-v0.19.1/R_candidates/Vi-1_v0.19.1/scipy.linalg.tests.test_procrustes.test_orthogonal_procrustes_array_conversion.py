def test_orthogonal_procrustes_array_conversion():
    np.random.seed(1234)
    for m, n in ((6, 4), (4, 4), (4, 6)):
        A_arr = np.random.randn(m, n)
        B_arr = np.random.randn(m, n)
        As = (A_arr, A_arr.tolist(), np.matrix(A_arr))
        Bs = (B_arr, B_arr.tolist(), np.matrix(B_arr))
        R_arr, s = orthogonal_procrustes(A_arr, B_arr)
        AR_arr = A_arr.dot(R_arr)
        for A, B in product(As, Bs):
            R, s = orthogonal_procrustes(A, B)
            AR = A_arr.dot(R)
            assert_allclose(AR, AR_arr)
