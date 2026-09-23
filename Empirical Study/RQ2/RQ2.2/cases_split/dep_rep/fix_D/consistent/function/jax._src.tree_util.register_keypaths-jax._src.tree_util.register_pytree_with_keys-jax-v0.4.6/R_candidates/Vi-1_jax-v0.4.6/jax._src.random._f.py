@partial(jit, static_argnums=(3, 4), inline=True)
def _f(key, dfnum, dfden, shape, dtype) -> Array:
  if shape is None:
    shape =  lax.broadcast_shapes(np.shape(dfden), np.shape(dfnum))
  else:
    _check_shape("f", shape, np.shape(dfden), np.shape(dfnum))
  dfden = lax.convert_element_type(dfden, dtype)
  dfnum = lax.convert_element_type(dfnum, dtype)
  key_dfd, key_dfn = _split(key)
  chi2_dfn = chisquare(key_dfn, dfnum, shape, dtype)
  chi2_dfd = chisquare(key_dfd, dfden, shape, dtype)
  # broadcast dfden and dfnum to do div operation
  dfden = jnp.broadcast_to(dfden, shape)
  dfnum = jnp.broadcast_to(dfnum, shape)
  num = lax.div(chi2_dfn, dfnum)
  den = lax.div(chi2_dfd ,dfden)
  f = lax.div(num, den)
  return f
