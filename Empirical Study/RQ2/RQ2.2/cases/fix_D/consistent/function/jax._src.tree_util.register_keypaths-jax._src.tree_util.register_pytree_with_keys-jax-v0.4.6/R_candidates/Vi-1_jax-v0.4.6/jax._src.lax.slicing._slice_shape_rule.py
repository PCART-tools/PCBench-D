def _slice_shape_rule(operand, *, start_indices, limit_indices, strides):
  lax._check_shapelike("slice", "start_indices", start_indices)
  lax._check_shapelike("slice", "limit_indices", limit_indices)
  if operand.ndim != len(start_indices):
    msg = ("slice start_indices must have length equal to the number of "
           "dimensions of the operand, got indices {} for operand shape {}.")
    raise TypeError(msg.format(start_indices, operand.shape))
  if len(start_indices) != len(limit_indices):
    msg = ("slice limit_indices must have the same length as start_indices, "
           "got start_indices {} and limit_indices {}.")
    raise TypeError(msg.format(start_indices, limit_indices))
  if not core.greater_equal_shape(operand.shape, limit_indices):
    msg = ("slice limit_indices must be less than or equal to operand shape, "
           "got limit_indices {} for operand shape {}.")
    raise TypeError(msg.format(limit_indices, operand.shape))
  if not all(core.greater_equal_dim(si, 0) for si in start_indices):
    msg = ("slice start_indices must be greater than or equal to zero, "
           "got start_indices of {}.")
    raise TypeError(msg.format(start_indices))
  if not jax.config.jax_dynamic_shapes:
    if not core.greater_equal_shape(limit_indices, start_indices):
      msg = ("slice limit_indices must be greater than or equal to start_indices,"
            " got start_indices {} and limit_indices {}.")
      raise TypeError(msg.format(start_indices, limit_indices))
  if strides is None or tuple(strides) == (1,) * len(operand.shape):
    shape = [limit if type(start) is int and start == 0 else limit - start
             for start, limit in zip(start_indices, limit_indices)]
    return tuple(shape)

  lax._check_shapelike("slice", "strides", strides)
  if len(strides) != operand.ndim:
    msg = ("slice strides must have length equal to the number of dimensions "
            "of the operand, got strides {} for operand shape {}.")
    raise TypeError(msg.format(strides, operand.shape))
  if not core.greater_equal_shape(strides, (0,) * len(strides)):
    msg = "slice strides must be positive, got {}"
    raise TypeError(msg.format(strides))
  diff = core.diff_shape(limit_indices, start_indices)
  return core.stride_shape(diff, (1,) * len(diff), strides)
