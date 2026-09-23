def _gather_batching_rule(batched_args, batch_dims, *, dimension_numbers,
                          slice_sizes, unique_indices, indices_are_sorted,
                          mode, fill_value):
  operand, indices = batched_args
  operand_bdim, indices_bdim = batch_dims

  if operand_bdim is not None and indices_bdim is None:
    operand = batching.moveaxis(operand, operand_bdim, 0)
    slice_sizes = (operand.shape[0],) + slice_sizes
    offset_dims = (0,) + tuple(np.add(1, dimension_numbers.offset_dims))
    collapsed_slice_dims = tuple(np.add(1, dimension_numbers.collapsed_slice_dims))
    start_index_map = tuple(np.add(1, dimension_numbers.start_index_map))
    dnums = GatherDimensionNumbers(
        offset_dims=offset_dims,
        collapsed_slice_dims=collapsed_slice_dims,
        start_index_map=start_index_map)
    return gather(operand, indices, dimension_numbers=dnums,
                  slice_sizes=slice_sizes, unique_indices=unique_indices,
                  indices_are_sorted=indices_are_sorted, mode=mode,
                  fill_value=fill_value), 0

  elif operand_bdim is None and indices_bdim is not None:
    indices = batching.moveaxis(indices, indices_bdim, 0)
    offset_dims = tuple(np.add(1, dimension_numbers.offset_dims))
    dnums = GatherDimensionNumbers(
        offset_dims=offset_dims,
        collapsed_slice_dims=dimension_numbers.collapsed_slice_dims,
        start_index_map=dimension_numbers.start_index_map)
    # If batching indexed accesses into the same array, the batched gather may
    # no longer have sorted or unique indices.
    return gather(operand, indices, dimension_numbers=dnums,
                  slice_sizes=slice_sizes, unique_indices=False,
                  indices_are_sorted=False, mode=mode, fill_value=fill_value), 0

  else:
    # move batch dimensions to the front to simplify logic
    operand = batching.moveaxis(operand, operand_bdim, 0)
    indices = batching.moveaxis(indices, indices_bdim, 0)

    # This slightly awkward special case is needed because the shape rule for
    # gather does not allow size-1 slices out of a size-0 dimension, even if
    # the number of slices is zero. Likely the best fix would be to change the
    # definition of gather() so it can be batched without the construction of
    # an explicit iota of size-1 slices.
    if core.symbolic_equal_dim(operand.shape[0], 0):
      output_shape = _gather_shape_rule(
          core.ShapedArray(operand.shape[1:], operand.dtype),
          core.ShapedArray(indices.shape[1:],
                           dtypes.canonicalize_dtype(indices.dtype)),
          dimension_numbers=dimension_numbers, slice_sizes=slice_sizes,
          unique_indices=unique_indices, indices_are_sorted=indices_are_sorted,
          mode=mode, fill_value=fill_value)
      return lax.full((0,) + output_shape, lax._zero(operand)), 0

    # Example: user code had indices shape (3, 4, 5), and we have to deal with
    # indices shape (7, 3, 4, 5). We transform that to indices of shape
    # (7, 3, 4, 6) where we concatenated an iota that counts along our batch
    # dimension to the front of the ndindex.
    count_shape = list(indices.shape)
    count_shape[-1] = 1
    counts = lax.broadcasted_iota(indices.dtype, tuple(count_shape), 0)
    indices = lax.concatenate([counts, indices], len(count_shape) - 1)

    slice_sizes = (1,) + slice_sizes
    collapsed_slice_dims = (0,) + tuple(np.add(1, dimension_numbers.collapsed_slice_dims))
    offset_dims = tuple(np.add(1, dimension_numbers.offset_dims))
    start_index_map = (0,) + tuple(np.add(1, dimension_numbers.start_index_map))

    dnums = GatherDimensionNumbers(
        offset_dims=offset_dims,
        collapsed_slice_dims=collapsed_slice_dims,
        start_index_map=start_index_map)
    return gather(operand, indices, dimension_numbers=dnums,
                  slice_sizes=slice_sizes, unique_indices=unique_indices,
                  indices_are_sorted=indices_are_sorted, mode=mode,
                  fill_value=fill_value), 0
