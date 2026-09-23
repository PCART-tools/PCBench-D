@util._wraps(np.lexsort)
@partial(jit, static_argnames=('axis',))
def lexsort(keys, axis=-1):
  keys = tuple(keys)
  if len(keys) == 0:
    raise TypeError("need sequence of keys with len > 0 in lexsort")
  if len({shape(key) for key in keys}) > 1:
    raise ValueError("all keys need to be the same shape")
  if ndim(keys[0]) == 0:
    return array(0, dtype=dtypes.canonicalize_dtype(int_))
  axis = _canonicalize_axis(axis, ndim(keys[0]))
  use_64bit_index = keys[0].shape[axis] >= (1 << 31)
  iota = lax.broadcasted_iota(int64 if use_64bit_index else int_, shape(keys[0]), axis)
  return lax.sort((*keys[::-1], iota), dimension=axis, num_keys=len(keys))[-1]
