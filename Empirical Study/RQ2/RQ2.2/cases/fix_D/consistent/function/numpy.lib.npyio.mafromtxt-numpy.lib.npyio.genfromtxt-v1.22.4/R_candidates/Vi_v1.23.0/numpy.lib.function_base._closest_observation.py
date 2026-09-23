def _closest_observation(n, quantiles):
    gamma_fun = lambda gamma, index: (gamma == 0) & (np.floor(index) % 2 == 0)
    return _discret_interpolation_to_boundaries((n * quantiles) - 1 - 0.5,
                                                gamma_fun)
