def _clamp_scatter_indices(operand, indices, updates, *, dnums):
  """Clamps `indices` to be in-range for a scatter."""
  slice_sizes = []
  pos = 0
  for i in range(len(operand.shape)):
    if i in dnums.inserted_window_dims:
      slice_sizes.append(1)
    else:
      slice_sizes.append(updates.shape[dnums.update_window_dims[pos]])
      pos += 1

  upper_bounds: core.Shape = tuple(operand.shape[i] - slice_sizes[i]
                                   for i in dnums.scatter_dims_to_operand_dims)
  # Stack upper_bounds into a Array[n]
  upper_bound = lax.shape_as_value(upper_bounds)
  # This fix fails lax_test_no_jax_array
  upper_bound = lax.min(upper_bound,
                        lax.convert_element_type(np.uint64(np.iinfo(indices.dtype).max),
                                                  np.int64))

  upper_bound = lax.broadcast_in_dim(upper_bound, indices.shape,
                                     (len(indices.shape) - 1,))
  return lax.clamp(np.int64(0), lax.convert_element_type(indices, np.int64),
                   upper_bound)
