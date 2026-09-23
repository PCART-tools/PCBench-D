def _centered(A):
    mu = A.mean(axis=0)
    return A - mu, mu
