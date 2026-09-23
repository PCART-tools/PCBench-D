@_wraps(np.concatenate)
def concatenate(arrays, axis: int = 0):
  if isinstance(arrays, (np.ndarray, ndarray)):
    return _concatenate_array(arrays, axis)
  _stackable(*arrays) or _check_arraylike("concatenate", *arrays)
  if not len(arrays):
    raise ValueError("Need at least one array to concatenate.")
  if ndim(arrays[0]) == 0:
    raise ValueError("Zero-dimensional arrays cannot be concatenated.")
  if axis is None:
    return concatenate([ravel(a) for a in arrays], axis=0)
  if hasattr(arrays[0], "concatenate"):
    return arrays[0].concatenate(arrays[1:], axis)
  axis = _canonicalize_axis(axis, ndim(arrays[0]))
  arrays = _promote_dtypes(*arrays)
  # lax.concatenate can be slow to compile for wide concatenations, so form a
  # tree of concatenations as a workaround especially for op-by-op mode.
  # (https://github.com/google/jax/issues/653).
  k = 16
  if len(arrays) == 1:
    return asarray(arrays[0])
  else:
    while len(arrays) > 1:
      arrays = [lax.concatenate(arrays[i:i+k], axis)
                for i in range(0, len(arrays), k)]
    return arrays[0]
