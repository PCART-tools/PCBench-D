def test_orthogonal_procrustes_exact_example():
    # Check a small application.
    # It uses translation, scaling, reflection, and rotation.
    #
    #         |
    #   a  b  |
    #         |
    #   d  c  |        w
    #         |
    # --------+--- x ----- z ---
    #         |
    #         |        y
    #         |
    #
    A_orig = np.array([[-3, 3], [-2, 3], [-2, 2], [-3, 2]], dtype=float)
    B_orig = np.array([[3, 2], [1, 0], [3, -2], [5, 0]], dtype=float)
    A, A_mu = _centered(A_orig)
    B, B_mu = _centered(B_orig)
    R, s = orthogonal_procrustes(A, B)
    scale = s / np.square(norm(A))
    B_approx = scale * np.dot(A, R) + B_mu
    assert_allclose(B_approx, B_orig, atol=1e-8)
