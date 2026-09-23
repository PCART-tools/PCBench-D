def test_orthogonal_procrustes():
    np.random.seed(1234)
    for m, n in ((6, 4), (4, 4), (4, 6)):
        # Sample a random target matrix.
        B = np.random.randn(m, n)
        # Sample a random orthogonal matrix
        # by computing eigh of a sampled symmetric matrix.
        X = np.random.randn(n, n)
        w, V = eigh(X.T + X)
        assert_allclose(inv(V), V.T)
        # Compute a matrix with a known orthogonal transformation that gives B.
        A = np.dot(B, V.T)
        # Check that an orthogonal transformation from A to B can be recovered.
        R, s = orthogonal_procrustes(A, B)
        assert_allclose(inv(R), R.T)
        assert_allclose(A.dot(R), B)
        # Create a perturbed input matrix.
        A_perturbed = A + 1e-2 * np.random.randn(m, n)
        # Check that the orthogonal procrustes function can find an orthogonal
        # transformation that is better than the orthogonal transformation
        # computed from the original input matrix.
        R_prime, s = orthogonal_procrustes(A_perturbed, B)
        assert_allclose(inv(R_prime), R_prime.T)
        # Compute the naive and optimal transformations of the perturbed input.
        naive_approx = A_perturbed.dot(R)
        optim_approx = A_perturbed.dot(R_prime)
        # Compute the Frobenius norm errors of the matrix approximations.
        naive_approx_error = norm(naive_approx - B, ord='fro')
        optim_approx_error = norm(optim_approx - B, ord='fro')
        # Check that the orthogonal Procrustes approximation is better.
        assert_array_less(optim_approx_error, naive_approx_error)
