@partial(jit, static_argnums=(2, 3), inline=True)
def _pareto(key, b, shape, dtype):
  if shape is None:
    shape = np.shape(b)
  else:
    _check_shape("pareto", shape)

  b = lax.convert_element_type(b, dtype)
  e = exponential(key, shape, dtype)
  return lax.exp(e / b)
