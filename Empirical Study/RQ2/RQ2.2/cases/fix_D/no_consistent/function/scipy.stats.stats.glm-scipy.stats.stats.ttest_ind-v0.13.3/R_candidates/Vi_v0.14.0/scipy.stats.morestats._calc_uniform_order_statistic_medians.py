def _calc_uniform_order_statistic_medians(x):
    """See Notes section of `probplot` for details."""
    N = len(x)
    osm_uniform = np.zeros(N, dtype=np.float64)
    osm_uniform[-1] = 0.5**(1.0 / N)
    osm_uniform[0] = 1 - osm_uniform[-1]
    i = np.arange(2, N)
    osm_uniform[1:-1] = (i - 0.3175) / (N + 0.365)
    return osm_uniform
