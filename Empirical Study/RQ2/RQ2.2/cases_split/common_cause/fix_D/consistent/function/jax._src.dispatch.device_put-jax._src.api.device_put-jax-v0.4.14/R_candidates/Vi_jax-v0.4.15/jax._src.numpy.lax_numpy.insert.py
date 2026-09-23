@util._wraps(np.insert)
def insert(arr: ArrayLike, obj: ArrayLike | slice, values: ArrayLike,
           axis: int | None = None) -> Array:
  util.check_arraylike("insert", arr, 0 if isinstance(obj, slice) else obj, values)
  a = asarray(arr)
  values_arr = asarray(values)

  if axis is None:
    a = ravel(a)
    axis = 0
  axis = core.concrete_or_error(None, axis, "axis argument of jnp.insert()")
  axis = _canonicalize_axis(axis, a.ndim)
  if isinstance(obj, slice):
    indices = arange(*obj.indices(a.shape[axis]))
  else:
    indices = asarray(obj)

  if indices.ndim > 1:
    raise ValueError("jnp.insert(): obj must be a slice, a one-dimensional "
                     f"array, or a scalar; got {obj}")
  if not np.issubdtype(indices.dtype, np.integer):
    if indices.size == 0 and not isinstance(obj, Array):
      indices = indices.astype(int)
    else:
      # Note: np.insert allows boolean inputs but the behavior is deprecated.
      raise ValueError("jnp.insert(): index array must be "
                       f"integer typed; got {obj}")
  values_arr = array(values_arr, ndmin=a.ndim, dtype=a.dtype, copy=False)

  if indices.size == 1:
    index = ravel(indices)[0]
    if indices.ndim == 0:
      values_arr = moveaxis(values_arr, 0, axis)
    indices = full(values_arr.shape[axis], index)
  n_input = a.shape[axis]
  n_insert = broadcast_shapes(indices.shape, (values_arr.shape[axis],))[0]
  out_shape = list(a.shape)
  out_shape[axis] += n_insert
  out = zeros_like(a, shape=tuple(out_shape))

  indices = where(indices < 0, indices + n_input, indices)
  indices = clip(indices, 0, n_input)

  values_ind = indices.at[argsort(indices)].add(arange(n_insert, dtype=indices.dtype))
  arr_mask = ones(n_input + n_insert, dtype=bool).at[values_ind].set(False)
  arr_ind = where(arr_mask, size=n_input)[0]

  out = out.at[(slice(None),) * axis + (values_ind,)].set(values_arr)
  out = out.at[(slice(None),) * axis + (arr_ind,)].set(a)

  return out
