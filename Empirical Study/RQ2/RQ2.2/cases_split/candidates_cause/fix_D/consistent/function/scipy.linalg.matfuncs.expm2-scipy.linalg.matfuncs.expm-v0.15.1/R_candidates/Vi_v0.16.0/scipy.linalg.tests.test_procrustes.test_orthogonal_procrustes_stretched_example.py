def test_orthogonal_procrustes_stretched_example():
    # Try again with a target with a stretched y axis.
    A_orig = np.array([[-3, 3], [-2, 3], [-2, 2], [-3, 2]], dtype=float)
    B_orig = np.array([[3, 40], [1, 0], [3, -40], [5, 0]], dtype=float)
    A, A_mu = _centered(A_orig)
    B, B_mu = _centered(B_orig)
    R, s = orthogonal_procrustes(A, B)
    scale = s / np.square(norm(A))
    B_approx = scale * np.dot(A, R) + B_mu
    expected = np.array([[3, 21], [-18, 0], [3, -21], [24, 0]], dtype=float)
    assert_allclose(B_approx, expected, atol=1e-8)
    # Check disparity symmetry.
    expected_disparity = 0.4501246882793018
    AB_disparity = np.square(norm(B_approx - B_orig) / norm(B))
    assert_allclose(AB_disparity, expected_disparity)
    R, s = orthogonal_procrustes(B, A)
    scale = s / np.square(norm(B))
    A_approx = scale * np.dot(B, R) + A_mu
    BA_disparity = np.square(norm(A_approx - A_orig) / norm(A))
    assert_allclose(BA_disparity, expected_disparity)
