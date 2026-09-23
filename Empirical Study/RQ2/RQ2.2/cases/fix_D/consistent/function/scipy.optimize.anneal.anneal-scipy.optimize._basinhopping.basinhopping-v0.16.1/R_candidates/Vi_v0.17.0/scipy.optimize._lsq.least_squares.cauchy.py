def cauchy(z, rho, cost_only):
    rho[0] = np.log1p(z)
    if cost_only:
        return
    t = 1 + z
    rho[1] = 1 / t
    rho[2] = -1 / t**2
