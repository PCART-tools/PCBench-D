def _gather_fill(operand, indices, *, dimension_numbers, slice_sizes,
                 unique_indices, indices_are_sorted, fill_value,
                 output_shape):
  """Lowers a FILL_OR_DROP gather as a PROMISE_IN_BOUNDS gather with masking."""
  dnums = dimension_numbers
  intarray = partial(np.array, dtype=np.int64)
  operand_dims = lax.shape_as_value(operand.shape)
  indices = lax.convert_element_type(indices, np.int64)
  num_batch_dims = len(indices.shape) - 1

  upper_bound = (
      operand_dims[intarray(dnums.start_index_map)] -
      lax.shape_as_value(slice_sizes)[intarray(dnums.start_index_map)])
  mask = lax.bitwise_and(
      lax.ge(indices, np.int64(0)),
      lax.le(indices, lax.expand_dims(upper_bound, tuple(range(num_batch_dims)))))
  mask = lax._reduce_and(mask, [num_batch_dims])

  # Computes the output shape and the positions of the batch dimensions in the
  # output
  output_ndims = num_batch_dims + len(dnums.offset_dims)
  batch_dims_in_output = np.delete(np.arange(output_ndims),
                                   dnums.offset_dims)

  # We don't consume unique_indices directly in gather(), only in its transpose
  # (scatter).
  gather_out = gather(operand, indices, dnums, slice_sizes,
                      indices_are_sorted=indices_are_sorted,
                      mode=GatherScatterMode.PROMISE_IN_BOUNDS)
  return lax.select(
    lax.broadcast_in_dim(mask, output_shape, batch_dims_in_output),
    gather_out, lax.full_like(gather_out, fill_value=fill_value))
