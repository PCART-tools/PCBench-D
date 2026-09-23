@_wraps(osp_stats.nbinom.pmf, update_doc=False)
def pmf(k: ArrayLike, n: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
    """JAX implementation of scipy.stats.binom.pmf."""
    return lax.exp(logpmf(k, n, p, loc))
