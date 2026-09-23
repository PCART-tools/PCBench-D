def _broadcast_to(arr, shape):
  if hasattr(arr, "broadcast_to"):
    return arr.broadcast_to(shape)
  _check_arraylike("broadcast_to", arr)
  arr = arr if isinstance(arr, ndarray) else _asarray(arr)
  if not isinstance(shape, tuple) and np.ndim(shape) == 0:
    shape = (shape,)
  shape = core.canonicalize_shape(shape)  # check that shape is concrete
  arr_shape = np.shape(arr)
  if core.symbolic_equal_shape(arr_shape, shape):
    return arr
  else:
    nlead = len(shape) - len(arr_shape)
    shape_tail = shape[nlead:]
    compatible = all(core.symbolic_equal_one_of_dim(arr_d, [1, shape_d])
                     for arr_d, shape_d in safe_zip(arr_shape, shape_tail))
    if nlead < 0 or not compatible:
      msg = "Incompatible shapes for broadcasting: {} and requested shape {}"
      raise ValueError(msg.format(arr_shape, shape))
    diff, = np.where(tuple(not core.symbolic_equal_dim(arr_d, shape_d)
                           for arr_d, shape_d in safe_zip(arr_shape, shape_tail)))
    new_dims = tuple(range(nlead)) + tuple(nlead + diff)
    kept_dims = tuple(np.delete(np.arange(len(shape)), new_dims))
    return lax.broadcast_in_dim(lax.squeeze(arr, tuple(diff)), shape, kept_dims)
