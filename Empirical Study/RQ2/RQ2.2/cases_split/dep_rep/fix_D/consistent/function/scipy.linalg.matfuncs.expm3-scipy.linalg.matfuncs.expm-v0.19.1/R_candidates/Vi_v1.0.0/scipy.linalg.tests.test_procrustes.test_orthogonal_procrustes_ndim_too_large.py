def test_orthogonal_procrustes_ndim_too_large():
    np.random.seed(1234)
    A = np.random.randn(3, 4, 5)
    B = np.random.randn(3, 4, 5)
    assert_raises(ValueError, orthogonal_procrustes, A, B)
