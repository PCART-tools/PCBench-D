def test_orthogonal_procrustes_shape_mismatch():
    np.random.seed(1234)
    shapes = ((3, 3), (3, 4), (4, 3), (4, 4))
    for a, b in permutations(shapes, 2):
        A = np.random.randn(*a)
        B = np.random.randn(*b)
        assert_raises(ValueError, orthogonal_procrustes, A, B)
