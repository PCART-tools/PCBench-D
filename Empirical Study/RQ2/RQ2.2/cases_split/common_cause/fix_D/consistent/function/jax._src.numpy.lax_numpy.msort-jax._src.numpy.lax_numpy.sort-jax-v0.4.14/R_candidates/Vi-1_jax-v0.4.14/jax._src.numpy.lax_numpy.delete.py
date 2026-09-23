@util._wraps(np.delete,
  lax_description=_dedent("""
    delete() usually requires the index specification to be static. If the index
    is an integer array that is guaranteed to contain unique entries, you may
    specify ``assume_unique_indices=True`` to perform the operation in a
    manner that does not require static indices."""),
  extra_params=_dedent("""
    assume_unique_indices : int, optional (default=False)
        In case of array-like integer (not boolean) indices, assume the indices are unique,
        and perform the deletion in a way that is compatible with JIT and other JAX
        transformations."""))
def delete(arr, obj, axis=None, *, assume_unique_indices=False):
  util.check_arraylike("delete", arr)
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
    obj = arange(arr.shape[axis])[obj]
    assume_unique_indices = True

  # Case 3: obj is an array
  # NB: pass both arrays to check for appropriate error message.
  util.check_arraylike("delete", arr, obj)

  # Case 3a: unique integer indices; delete in a JIT-compatible way
  if issubdtype(_dtype(obj), integer) and assume_unique_indices:
    obj = asarray(obj).ravel()
    obj = clip(where(obj < 0, obj + arr.shape[axis], obj), 0, arr.shape[axis])
    obj = sort(obj)
    obj -= arange(len(obj))
    i = arange(arr.shape[axis] - obj.size)
    i += (i[None, :] >= obj[:, None]).sum(0)
    return arr[(slice(None),) * axis + (i,)]

  # Case 3b: non-unique indices: must be static.
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
