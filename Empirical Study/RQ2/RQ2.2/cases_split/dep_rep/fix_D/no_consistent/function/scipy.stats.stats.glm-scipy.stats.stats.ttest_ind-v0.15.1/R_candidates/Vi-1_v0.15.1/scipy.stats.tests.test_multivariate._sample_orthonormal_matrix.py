def _sample_orthonormal_matrix(n):
    M = np.random.randn(n, n)
    u, s, v = scipy.linalg.svd(M)
    return u
