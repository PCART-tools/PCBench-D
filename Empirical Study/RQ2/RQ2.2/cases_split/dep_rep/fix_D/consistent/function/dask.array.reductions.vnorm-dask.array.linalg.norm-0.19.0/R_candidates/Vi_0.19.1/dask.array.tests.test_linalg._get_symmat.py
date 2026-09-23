def _get_symmat(size):
    np.random.seed(1)
    A = np.random.randint(1, 21, (size, size))
    lA = np.tril(A)
    return lA.dot(lA.T)
