def _cholesky_lower(a):
    import scipy.linalg
    return scipy.linalg.cholesky(a, lower=True)
