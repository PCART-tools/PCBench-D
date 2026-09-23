@partial(jit, static_argnums=(2, 3))
def _chisquare(key, df, shape, dtype) -> Array:
  if shape is None:
    shape = np.shape(df)
  else:
    _check_shape("chisquare", shape, np.shape(df))
  df = lax.convert_element_type(df, dtype)
  two = _lax_const(df, 2)
  half_df = lax.div(df, two)
  log_g = loggamma(key, a=half_df, shape=shape, dtype=dtype)
  chi2 = lax.mul(jnp.exp(log_g), two)
  return chi2
