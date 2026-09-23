def _get_symmat(size):
    np.random.seed(1)
    A = np.random.random_integers(1, 20, (size, size))
    lA = np.tril(A)
    return lA.dot(lA.T)
