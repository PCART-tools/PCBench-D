@_wraps(np.insert)
def insert(arr, obj, values, axis=None):
  _check_arraylike("insert", arr, 0 if isinstance(obj, slice) else obj, values)
  arr = asarray(arr)
  values = asarray(values)

  if axis is None:
    arr = ravel(arr)
    axis = 0
  axis = core.concrete_or_error(None, axis, "axis argument of jnp.insert()")
  axis = _canonicalize_axis(axis, arr.ndim)
  if isinstance(obj, slice):
    indices = arange(*obj.indices(arr.shape[axis]))
  else:
    indices = asarray(obj)

  if indices.ndim > 1:
    raise ValueError("jnp.insert(): obj must be a slice, a one-dimensional "
                     f"array, or a scalar; got {obj}")
  if not np.issubdtype(indices.dtype, np.integer):
    if indices.size == 0 and not isinstance(obj, ndarray):
      indices = indices.astype(int)
    else:
      # Note: np.insert allows boolean inputs but the behavior is deprecated.
      raise ValueError("jnp.insert(): index array must be "
                       f"integer typed; got {obj}")
  values = array(values, ndmin=arr.ndim, dtype=arr.dtype, copy=False)

  if indices.size == 1:
    index = ravel(indices)[0]
    if indices.ndim == 0:
      values = moveaxis(values, 0, axis)
    indices = full(values.shape[axis], index)
  n_input = arr.shape[axis]
  n_insert = broadcast_shapes(indices.shape, values.shape[axis])[0]
  out_shape = list(arr.shape)
  out_shape[axis] += n_insert
  out = zeros_like(arr, shape=tuple(out_shape))

  indices = where(indices < 0, indices + n_input, indices)
  indices = clip(indices, 0, n_input)

  values_ind = indices.at[argsort(indices)].add(arange(n_insert, dtype=indices.dtype))
  arr_mask = ones(n_input + n_insert, dtype=bool).at[values_ind].set(False)
  arr_ind = where(arr_mask, size=n_input)[0]

  out = out.at[(slice(None),) * axis + (values_ind,)].set(values)
  out = out.at[(slice(None),) * axis + (arr_ind,)].set(arr)

  return out
