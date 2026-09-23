def stirling_series(N):
    coeffs = []
    with mpmath.workdps(100):
        for n in range(1, N + 1):
            coeffs.append(mpmath.bernoulli(2*n)/(2*n*(2*n - 1)))
    return coeffs
