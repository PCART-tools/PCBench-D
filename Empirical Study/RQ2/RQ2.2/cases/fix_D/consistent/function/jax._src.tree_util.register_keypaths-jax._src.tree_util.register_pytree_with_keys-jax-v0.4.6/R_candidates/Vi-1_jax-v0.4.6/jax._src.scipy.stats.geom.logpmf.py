@_wraps(osp_stats.geom.logpmf, update_doc=False)
def logpmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
    k, p, loc = _promote_args_inexact("geom.logpmf", k, p, loc)
    zero = _lax_const(k, 0)
    one = _lax_const(k, 1)
    x = lax.sub(k, loc)
    log_probs = xlog1py(lax.sub(x, one), -p) + lax.log(p)
    return jnp.where(lax.le(x, zero), -jnp.inf, log_probs)
