def test_orthogonal_procrustes_checkfinite_exception():
    np.random.seed(1234)
    m, n = 2, 3
    A_good = np.random.randn(m, n)
    B_good = np.random.randn(m, n)
    for bad_value in np.inf, -np.inf, np.nan:
        A_bad = A_good.copy()
        A_bad[1, 2] = bad_value
        B_bad = B_good.copy()
        B_bad[1, 2] = bad_value
        for A, B in ((A_good, B_bad), (A_bad, B_good), (A_bad, B_bad)):
            assert_raises(ValueError, orthogonal_procrustes, A, B)
