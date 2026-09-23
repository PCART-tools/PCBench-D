def _broadcast_to(arr: ArrayLike, shape: DimSize | Shape) -> Array:
  check_arraylike("broadcast_to", arr)
  arr = arr if isinstance(arr, Array) else lax.asarray(arr)
  if not isinstance(shape, tuple) and np.ndim(shape) == 0:
    shape = (shape,)
  # check that shape is concrete
  shape = core.canonicalize_shape(shape)  # type: ignore[arg-type]
  arr_shape = np.shape(arr)
  if core.definitely_equal_shape(arr_shape, shape):
    return arr
  elif len(shape) < len(arr_shape):
    raise ValueError(f"Cannot broadcast to shape with fewer dimensions: {arr_shape=} {shape=}")
  else:
    nlead = len(shape) - len(arr_shape)
    shape_tail = shape[nlead:]
    compatible = all(core.definitely_equal_one_of_dim(arr_d, [1, shape_d])
                     for arr_d, shape_d in safe_zip(arr_shape, shape_tail))
    if nlead < 0 or not compatible:
      msg = "Incompatible shapes for broadcasting: {} and requested shape {}"
      raise ValueError(msg.format(arr_shape, shape))
    return lax.broadcast_in_dim(arr, shape, tuple(range(nlead, len(shape))))
