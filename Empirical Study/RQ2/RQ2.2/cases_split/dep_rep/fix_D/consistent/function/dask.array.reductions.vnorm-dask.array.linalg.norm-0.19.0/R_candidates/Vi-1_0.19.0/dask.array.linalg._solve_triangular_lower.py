def _solve_triangular_lower(a, b):
    import scipy.linalg
    return scipy.linalg.solve_triangular(a, b, lower=True)
