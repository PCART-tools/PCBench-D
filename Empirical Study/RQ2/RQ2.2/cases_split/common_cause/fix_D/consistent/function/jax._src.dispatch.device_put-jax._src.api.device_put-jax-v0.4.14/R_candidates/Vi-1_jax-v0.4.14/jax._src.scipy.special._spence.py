def _spence(x: Array) -> Array:
  return jnp.piecewise(x,
                       [x < 0.0, x == 1.0, x == 0.0],
                       [jnp.nan, 0, jnp.pi ** 2 / 6, _spence_calc])
