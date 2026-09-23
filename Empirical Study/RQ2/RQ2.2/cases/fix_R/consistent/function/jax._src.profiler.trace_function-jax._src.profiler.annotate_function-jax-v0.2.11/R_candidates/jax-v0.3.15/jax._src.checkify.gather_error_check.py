def gather_error_check(error, enabled_errors, operand, start_indices, *,
                       dimension_numbers, slice_sizes, unique_indices,
                       indices_are_sorted, mode, fill_value):
  out = lax.gather_p.bind(
      operand, start_indices, dimension_numbers=dimension_numbers,
      slice_sizes=slice_sizes, unique_indices=unique_indices,
      indices_are_sorted=indices_are_sorted, mode=mode, fill_value=fill_value)

  if ErrorCategory.OOB not in enabled_errors:
    return out, error

  # compare to OOB masking logic in lax._gather_translation_rule
  dnums = dimension_numbers
  operand_dims = np.array(operand.shape)
  num_batch_dims = len(start_indices.shape) - 1

  upper_bound = operand_dims[np.array(dnums.start_index_map)]
  upper_bound -= np.array(slice_sizes)[np.array(dnums.start_index_map)]
  upper_bound = jnp.expand_dims(upper_bound, axis=tuple(range(num_batch_dims)))
  in_bounds = (start_indices >= 0) & (start_indices <= upper_bound.astype(start_indices.dtype))

  # Get first OOB index, axis and axis size so it can be added to the error msg.
  flat_idx = jnp.argmin(in_bounds)
  multi_idx = jnp.unravel_index(flat_idx, start_indices.shape)
  oob_axis = jnp.array(dnums.start_index_map)[multi_idx[-1]]
  oob_axis_size = jnp.array(operand.shape)[oob_axis]
  oob_index = jnp.ravel(start_indices)[flat_idx]
  payload = jnp.array([oob_index, oob_axis, oob_axis_size], dtype=jnp.int32)

  msg = (f'out-of-bounds indexing at {summary()} for array of '
         f'shape {operand.shape}: '
         'index {payload0} is out of bounds for axis {payload1} '
         'with size {payload2}.')

  return out, assert_func(error, jnp.all(in_bounds), msg, payload)
