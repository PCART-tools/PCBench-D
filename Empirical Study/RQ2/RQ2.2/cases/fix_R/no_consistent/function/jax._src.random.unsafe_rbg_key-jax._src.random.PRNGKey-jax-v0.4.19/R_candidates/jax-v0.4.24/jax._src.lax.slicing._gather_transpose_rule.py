def _gather_transpose_rule(t, operand, indices, *, dimension_numbers,
                           slice_sizes, unique_indices, indices_are_sorted,
                           mode, fill_value):
  assert ad.is_undefined_primal(operand)
  operand_shape = operand.aval.shape
  if type(t) is ad_util.Zero:
    out = ad_util.Zero(operand.aval)
  else:
    zeros = lax.full(operand_shape, lax._zero(t))
    scatter_dnums = ScatterDimensionNumbers(
      update_window_dims=dimension_numbers.offset_dims,
      inserted_window_dims=dimension_numbers.collapsed_slice_dims,
      scatter_dims_to_operand_dims=dimension_numbers.start_index_map)
    out = scatter_add(zeros, indices, t, scatter_dnums,
                      unique_indices=unique_indices,
                      indices_are_sorted=indices_are_sorted,
                      mode=mode)
  return [out, None]
