def _masked(padded_value, logical_shape, dimensions, value=0):
  """
  Sets all padding to the given value (default is 0) in the given dimensions.
  All values outside the logical shape are considered padding.
  """
  if len(dimensions) == 0:
    return padded_value

  masks = [broadcasted_iota(np.int32, padded_value.shape, d) < logical_shape[d]
           for d in dimensions]
  mask_intersection = masks[0]
  for mask in masks[1:]:
    mask_intersection &= mask
  return select(mask_intersection, padded_value, full_like(padded_value, value))
