def _gather_lower(ctx, operand, indices, *,
                  dimension_numbers, slice_sizes, unique_indices,
                  indices_are_sorted, mode, fill_value):
  aval_out, = ctx.avals_out
  if mode == GatherScatterMode.FILL_OR_DROP:
    gather_fill_fn = mlir.lower_fun(_gather_fill, multiple_results=False)
    return gather_fill_fn(
        ctx, operand, indices,
        dimension_numbers=dimension_numbers, slice_sizes=slice_sizes,
        unique_indices=unique_indices, indices_are_sorted=indices_are_sorted,
        fill_value=fill_value, output_shape=aval_out.shape)

  assert mode in (GatherScatterMode.PROMISE_IN_BOUNDS,
                  GatherScatterMode.CLIP), mode
  dnums = mhlo.GatherDimensionNumbers.get(
    collapsed_slice_dims=list(dimension_numbers.collapsed_slice_dims),
    index_vector_dim=len(ctx.avals_in[1].shape) - 1,
    offset_dims=list(dimension_numbers.offset_dims),
    start_index_map=list(dimension_numbers.start_index_map))
  return mhlo.GatherOp(
      operand,
      indices,
      dnums,
      mlir.dense_int_elements(slice_sizes),
      indices_are_sorted=ir.BoolAttr.get(indices_are_sorted)).results
