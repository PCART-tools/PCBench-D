def arctan(z, rho, cost_only):
    rho[0] = np.arctan(z)
    if cost_only:
        return
    t = 1 + z**2
    rho[1] = 1 / t
    rho[2] = -2 * z / t**2
