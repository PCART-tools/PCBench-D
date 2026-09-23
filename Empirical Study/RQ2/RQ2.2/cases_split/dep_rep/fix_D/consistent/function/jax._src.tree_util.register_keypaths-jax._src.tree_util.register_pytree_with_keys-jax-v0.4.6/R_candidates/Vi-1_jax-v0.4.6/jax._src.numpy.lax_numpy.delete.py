@util._wraps(np.delete)
def delete(arr, obj, axis=None):
  util._check_arraylike("delete", arr)
  if axis is None:
    arr = ravel(arr)
    axis = 0
  axis = _canonicalize_axis(axis, arr.ndim)

  # Case 1: obj is a static integer.
  try:
    obj = operator.index(obj)
    obj = _canonicalize_axis(obj, arr.shape[axis])
  except TypeError:
    pass
  else:
    idx = tuple(slice(None) for i in range(axis))
    return concatenate([arr[idx + (slice(0, obj),)], arr[idx + (slice(obj + 1, None),)]], axis=axis)

  # Case 2: obj is a static slice.
  if isinstance(obj, slice):
    # TODO(jakevdp): we should be able to do this dynamically with care.
    indices = np.delete(np.arange(arr.shape[axis]), obj)
    return take(arr, indices, axis=axis)

  # Case 3: obj is an array
  # NB: pass both arrays to check for appropriate error message.
  util._check_arraylike("delete", arr, obj)
  obj = core.concrete_or_error(np.asarray, obj, "'obj' array argument of jnp.delete()")

  if issubdtype(obj.dtype, integer):
    # TODO(jakevdp): in theory this could be done dynamically if obj has no duplicates,
    # but this would require the complement of lax.gather.
    mask = np.ones(arr.shape[axis], dtype=bool)
    mask[obj] = False
  elif obj.dtype == bool:
    if obj.shape != (arr.shape[axis],):
      raise ValueError("np.delete(arr, obj): for boolean indices, obj must be one-dimensional "
                       "with length matching specified axis.")
    mask = ~obj
  else:
    raise ValueError(f"np.delete(arr, obj): got obj.dtype={obj.dtype}; must be integer or bool.")
  return arr[tuple(slice(None) for i in range(axis)) + (mask,)]
