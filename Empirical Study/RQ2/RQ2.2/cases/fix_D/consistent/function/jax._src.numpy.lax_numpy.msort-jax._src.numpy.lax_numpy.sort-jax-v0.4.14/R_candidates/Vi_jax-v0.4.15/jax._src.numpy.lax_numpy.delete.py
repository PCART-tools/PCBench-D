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
def delete(
    arr: ArrayLike,
    obj: ArrayLike | slice,
    axis: int | None = None,
    *,
    assume_unique_indices: bool = False,
) -> Array:
  util.check_arraylike("delete", arr)
  if axis is None:
    arr = ravel(arr)
    axis = 0
  a = asarray(arr)
  axis = _canonicalize_axis(axis, a.ndim)

  # Case 1: obj is a static integer.
  try:
    obj = operator.index(obj)  # type: ignore[arg-type]
    obj = _canonicalize_axis(obj, a.shape[axis])
  except TypeError:
    pass
  else:
    idx = tuple(slice(None) for i in range(axis))
    return concatenate([a[idx + (slice(0, obj),)], a[idx + (slice(obj + 1, None),)]], axis=axis)

  # Case 2: obj is a static slice.
  if isinstance(obj, slice):
    obj = arange(a.shape[axis])[obj]
    assume_unique_indices = True

  # Case 3: obj is an array
  # NB: pass both arrays to check for appropriate error message.
  util.check_arraylike("delete", a, obj)

  # Case 3a: unique integer indices; delete in a JIT-compatible way
  if issubdtype(_dtype(obj), integer) and assume_unique_indices:
    obj = asarray(obj).ravel()
    obj = clip(where(obj < 0, obj + a.shape[axis], obj), 0, a.shape[axis])
    obj = sort(obj)
    obj -= arange(len(obj))  # type: ignore[arg-type,operator]
    i = arange(a.shape[axis] - obj.size)
    i += (i[None, :] >= obj[:, None]).sum(0)
    return a[(slice(None),) * axis + (i,)]

  # Case 3b: non-unique indices: must be static.
  obj_array = core.concrete_or_error(np.asarray, obj, "'obj' array argument of jnp.delete()")
  if issubdtype(obj_array.dtype, integer):
    # TODO(jakevdp): in theory this could be done dynamically if obj has no duplicates,
    # but this would require the complement of lax.gather.
    mask = np.ones(a.shape[axis], dtype=bool)
    mask[obj_array] = False
  elif obj_array.dtype == bool:
    if obj_array.shape != (a.shape[axis],):
      raise ValueError("np.delete(arr, obj): for boolean indices, obj must be one-dimensional "
                       "with length matching specified axis.")
    mask = ~obj_array
  else:
    raise ValueError(f"np.delete(arr, obj): got obj.dtype={obj_array.dtype}; must be integer or bool.")
  return a[tuple(slice(None) for i in range(axis)) + (mask,)]
