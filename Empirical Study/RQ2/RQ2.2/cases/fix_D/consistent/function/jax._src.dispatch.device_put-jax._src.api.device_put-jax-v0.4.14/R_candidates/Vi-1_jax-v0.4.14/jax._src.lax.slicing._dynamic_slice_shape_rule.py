def _dynamic_slice_shape_rule(
    operand, *starts_and_dyn_sizes, slice_sizes):
  start_indices, dyn = util.split_list(starts_and_dyn_sizes, [operand.ndim])
  if operand.ndim != len(start_indices):
    msg = ("dynamic_slice start_indices must have length equal to the number "
           "of dimensions of the operand, got indices {} for operand shape {}.")
    raise TypeError(msg.format(start_indices, operand.shape))
  if len(start_indices) != len(slice_sizes):
    msg = ("dynamic_slice slice_sizes must have the same length as "
           "start_indices, got start_indices length {} and slice_sizes {}.")
    raise TypeError(msg.format(len(start_indices), slice_sizes))
  if not dyn and not all(map(operator.ge, operand.shape, slice_sizes)):
    msg = ("slice slice_sizes must be less than or equal to operand shape, "
           "got slice_sizes {} for operand shape {}.")
    raise TypeError(msg.format(slice_sizes, operand.shape))
  if not dyn and not all(ssz >= 0 for ssz in slice_sizes):
    msg = ("slice slice_sizes must be greater than or equal to zero, "
           "got slice_sizes of {}.")
    raise TypeError(msg.format(slice_sizes))
  if any(idx.ndim != 0 for idx in start_indices):
    raise TypeError("start_indices arguments to dynamic_slice must be scalars, "
                    f" got indices {start_indices}")
  return tuple(lax._merge_dyn_shape(slice_sizes, dyn))
