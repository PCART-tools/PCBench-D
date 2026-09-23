def betaln(a: ArrayLike, b: ArrayLike) -> Array:
    """Compute the log of the beta function.

    Derived from scipy's implementation of `betaln`_.

    This implementation does not handle all branches of the scipy implementation, but is still much more accurate
    than just doing lgamma(a) + lgamma(b) - lgamma(a + b) when inputs are large (> 1M or so).

    .. _betaln:
        https://github.com/scipy/scipy/blob/ef2dee592ba8fb900ff2308b9d1c79e4d6a0ad8b/scipy/special/cdflib/betaln.f
    """
    a, b = _promote_args_inexact("betaln", a, b)
    a, b = jnp.minimum(a, b), jnp.maximum(a, b)
    small_b = lax.lgamma(a) + (lax.lgamma(b) - lax.lgamma(a + b))
    large_b = lax.lgamma(a) + algdiv(a, b)
    return jnp.where(b < 8, small_b, large_b)
