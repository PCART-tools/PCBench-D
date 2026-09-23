@partial(jit, static_argnums=(2, 3), inline=True)
def _t(key, df, shape, dtype) -> Array:
  if shape is None:
    shape = np.shape(df)
  else:
    _check_shape("t", shape, np.shape(df))

  df = lax.convert_element_type(df, dtype)
  key_n, key_g = _split(key)
  n = normal(key_n, shape, dtype)
  two = _lax_const(n, 2)
  half_df = lax.div(df, two)
  g = gamma(key_g, half_df, shape, dtype)
  return n * jnp.sqrt(half_df / g)
