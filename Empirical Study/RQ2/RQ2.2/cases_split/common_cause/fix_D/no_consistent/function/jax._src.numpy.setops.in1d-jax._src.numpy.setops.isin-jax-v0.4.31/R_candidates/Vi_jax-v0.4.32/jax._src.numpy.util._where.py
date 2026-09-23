@api.jit
def _where(condition: ArrayLike, x: ArrayLike, y: ArrayLike) -> Array:
  if x is None or y is None:
    raise ValueError("Either both or neither of the x and y arguments should "
                     "be provided to jax.numpy.where, got {} and {}."
                     .format(x, y))
  if not np.issubdtype(_dtype(condition), np.bool_):
    condition = lax.ne(condition, lax._zero(condition))
  x, y = promote_dtypes(x, y)
  if np.ndim(condition) == 0:
    # lax.select() handles scalar conditions without broadcasting.
    x_arr, y_arr = _broadcast_arrays(x, y)
  else:
    condition, x_arr, y_arr = _broadcast_arrays(condition, x, y)
  try:
    is_always_empty = core.is_empty_shape(x_arr.shape)
  except:
    is_always_empty = False  # can fail with dynamic shapes
  return lax.select(condition, x_arr, y_arr) if not is_always_empty else x_arr
