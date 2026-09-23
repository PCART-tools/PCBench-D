@implements(osp_stats.nbinom.logpmf, update_doc=False)
def logpmf(k: ArrayLike, n: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
    """JAX implementation of scipy.stats.binom.logpmf."""
    k, n, p, loc = promote_args_inexact("binom.logpmf", k, n, p, loc)
    y = lax.sub(k, loc)
    comb_term = lax.sub(
        gammaln(n + 1),
        lax.add(gammaln(y + 1), gammaln(n - y + 1))
    )
    log_linear_term = lax.add(xlogy(y, p), xlog1py(lax.sub(n, y), lax.neg(p)))
    log_probs = lax.add(comb_term, log_linear_term)
    return jnp.where(lax.ge(k, loc) & lax.lt(k, loc + n + 1), log_probs, -jnp.inf)
