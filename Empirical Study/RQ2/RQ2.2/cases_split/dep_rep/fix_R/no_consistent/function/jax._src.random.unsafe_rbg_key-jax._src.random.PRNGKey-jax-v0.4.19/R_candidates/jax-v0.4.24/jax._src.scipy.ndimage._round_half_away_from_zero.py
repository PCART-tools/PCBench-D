def _round_half_away_from_zero(a: Array) -> Array:
  return a if jnp.issubdtype(a.dtype, jnp.integer) else lax.round(a)
