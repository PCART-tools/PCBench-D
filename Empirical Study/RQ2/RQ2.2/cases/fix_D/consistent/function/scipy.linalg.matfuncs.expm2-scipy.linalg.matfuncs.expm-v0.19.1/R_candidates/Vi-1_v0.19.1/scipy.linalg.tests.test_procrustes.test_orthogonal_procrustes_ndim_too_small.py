def test_orthogonal_procrustes_ndim_too_small():
    np.random.seed(1234)
    A = np.random.randn(3)
    B = np.random.randn(3)
    assert_raises(ValueError, orthogonal_procrustes, A, B)
