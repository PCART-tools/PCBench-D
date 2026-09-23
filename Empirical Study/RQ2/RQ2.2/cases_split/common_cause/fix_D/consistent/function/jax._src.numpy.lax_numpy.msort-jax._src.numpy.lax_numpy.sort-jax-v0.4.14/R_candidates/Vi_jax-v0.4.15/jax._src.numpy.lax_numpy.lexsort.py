@util._wraps(np.lexsort)
@partial(jit, static_argnames=('axis',))
def lexsort(keys: Sequence[ArrayLike], axis: int = -1) -> Array:
  keys_arrays = tuple(asarray(k) for k in keys)
  if len(keys_arrays) == 0:
    raise TypeError("need sequence of keys with len > 0 in lexsort")
  if len({shape(key) for key in keys_arrays}) > 1:
    raise ValueError("all keys need to be the same shape")
  if ndim(keys_arrays[0]) == 0:
    return array(0, dtype=dtypes.canonicalize_dtype(int_))
  axis = _canonicalize_axis(axis, ndim(keys_arrays[0]))
  use_64bit_index = keys_arrays[0].shape[axis] >= (1 << 31)
  iota = lax.broadcasted_iota(int64 if use_64bit_index else int_, shape(keys_arrays[0]), axis)
  return lax.sort((*keys_arrays[::-1], iota), dimension=axis, num_keys=len(keys))[-1]
