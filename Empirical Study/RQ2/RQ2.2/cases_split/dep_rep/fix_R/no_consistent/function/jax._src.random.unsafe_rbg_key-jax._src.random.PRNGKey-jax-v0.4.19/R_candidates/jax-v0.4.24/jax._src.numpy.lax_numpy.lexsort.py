@util.implements(np.lexsort)
@partial(jit, static_argnames=('axis',))
def lexsort(keys: Array | np.ndarray | Sequence[ArrayLike], axis: int = -1) -> Array:
  key_tuple = tuple(keys)
  # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
  util.check_arraylike("lexsort", *key_tuple, emit_warning=True)
  key_arrays = tuple(asarray(k) for k in key_tuple)
  if len(key_arrays) == 0:
    raise TypeError("need sequence of keys with len > 0 in lexsort")
  if len({shape(key) for key in key_arrays}) > 1:
    raise ValueError("all keys need to be the same shape")
  if ndim(key_arrays[0]) == 0:
    return array(0, dtype=dtypes.canonicalize_dtype(int_))
  axis = _canonicalize_axis(axis, ndim(key_arrays[0]))
  use_64bit_index = key_arrays[0].shape[axis] >= (1 << 31)
  iota = lax.broadcasted_iota(int64 if use_64bit_index else int_, shape(key_arrays[0]), axis)
  return lax.sort((*key_arrays[::-1], iota), dimension=axis, num_keys=len(key_arrays))[-1]
