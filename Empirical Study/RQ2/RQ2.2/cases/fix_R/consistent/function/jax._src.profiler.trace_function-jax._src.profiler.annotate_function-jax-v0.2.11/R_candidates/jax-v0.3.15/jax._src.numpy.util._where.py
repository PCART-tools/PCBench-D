@api.jit
def _where(condition, x=None, y=None):
  if x is None or y is None:
    raise ValueError("Either both or neither of the x and y arguments should "
                     "be provided to jax.numpy.where, got {} and {}."
                     .format(x, y))
  if not np.issubdtype(_dtype(condition), np.bool_):
    condition = lax.ne(condition, lax_internal._zero(condition))
  x, y = _promote_dtypes(x, y)
  condition, x, y = _broadcast_arrays(condition, x, y)
  try: is_always_empty = core.is_empty_shape(np.shape(x))
  except: is_always_empty = False  # can fail with dynamic shapes
  return lax.select(condition, x, y) if not is_always_empty else x
