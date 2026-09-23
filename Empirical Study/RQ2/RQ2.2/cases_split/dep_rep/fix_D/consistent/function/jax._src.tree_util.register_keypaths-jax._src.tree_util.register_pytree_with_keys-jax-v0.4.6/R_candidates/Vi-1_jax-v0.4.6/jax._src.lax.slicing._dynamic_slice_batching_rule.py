def _dynamic_slice_batching_rule(batched_args, batch_dims, *, slice_sizes):
  # A dynamic slice is a special case of gather; we can delegate to the gather
  # batching rule.
  # TODO(phawkins): consider removing dynamic_slice entirely and using gather
  # always.
  operand, *start_indices = batched_args
  operand_bd, *start_idx_bds = batch_dims
  operand_shape = (operand.shape if operand_bd is batching.not_mapped
                   else tuple(np.delete(operand.shape, operand_bd)))
  dims = tuple(range(len(operand_shape)))
  dnums = GatherDimensionNumbers(offset_dims=dims, collapsed_slice_dims=(),
                                 start_index_map=dims)
  index, index_bdim = _batch_dynamic_slice_indices(start_indices, start_idx_bds)
  return _gather_batching_rule(
    [operand, index], [operand_bd, index_bdim], dimension_numbers=dnums,
    slice_sizes=slice_sizes, unique_indices=True, indices_are_sorted=True,
    mode=GatherScatterMode.PROMISE_IN_BOUNDS, fill_value=None)
