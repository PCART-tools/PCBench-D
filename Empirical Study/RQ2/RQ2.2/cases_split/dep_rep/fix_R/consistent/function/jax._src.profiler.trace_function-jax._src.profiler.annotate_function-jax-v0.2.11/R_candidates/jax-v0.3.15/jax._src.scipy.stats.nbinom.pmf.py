@_wraps(osp_stats.nbinom.pmf, update_doc=False)
def pmf(k, n, p, loc=0):
    """JAX implementation of scipy.stats.nbinom.pmf."""
    return lax.exp(logpmf(k, n, p, loc))
