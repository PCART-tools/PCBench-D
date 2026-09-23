@util._wraps(np.concatenate)
def concatenate(arrays: Union[np.ndarray, Array, Sequence[ArrayLike]],
                axis: Optional[int] = 0, dtype: Optional[DTypeLike] = None) -> Array:
  if isinstance(arrays, (np.ndarray, Array)):
    return _concatenate_array(arrays, axis, dtype=dtype)
  util._stackable(*arrays) or util.check_arraylike("concatenate", *arrays)
  if not len(arrays):
    raise ValueError("Need at least one array to concatenate.")
  if ndim(arrays[0]) == 0:
    raise ValueError("Zero-dimensional arrays cannot be concatenated.")
  if axis is None:
    return concatenate([ravel(a) for a in arrays], axis=0, dtype=dtype)
  if hasattr(arrays[0], "concatenate"):
    return arrays[0].concatenate(arrays[1:], axis, dtype=dtype)  # type: ignore[union-attr]
  axis = _canonicalize_axis(axis, ndim(arrays[0]))
  if dtype is None:
    arrays_out = util.promote_dtypes(*arrays)
  else:
    arrays_out = [asarray(arr, dtype=dtype) for arr in arrays]
  # lax.concatenate can be slow to compile for wide concatenations, so form a
  # tree of concatenations as a workaround especially for op-by-op mode.
  # (https://github.com/google/jax/issues/653).
  k = 16
  while len(arrays_out) > 1:
    arrays_out = [lax.concatenate(arrays_out[i:i+k], axis)
                  for i in range(0, len(arrays_out), k)]
  return arrays_out[0]
