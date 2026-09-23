@_wraps(osp_stats.nbinom.logpmf, update_doc=False)
def logpmf(k, n, p, loc=0):
    """JAX implementation of scipy.stats.nbinom.logpmf."""
    k, n, p, loc = _promote_args_inexact("nbinom.logpmf", k, n, p, loc)
    one = _lax_const(k, 1)
    y = lax.sub(k, loc)
    comb_term = lax.sub(
        lax.sub(gammaln(lax.add(y, n)), gammaln(n)), gammaln(lax.add(y, one))
    )
    log_linear_term = lax.add(xlogy(n, p), xlogy(y, lax.sub(one, p)))
    log_probs = lax.add(comb_term, log_linear_term)
    return where(lax.lt(k, loc), -inf, log_probs)
