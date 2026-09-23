def _dot_general_batch_rule(batched_args, batch_dims, *, dimension_numbers,
                            precision,
                            preferred_element_type: DTypeLike | None):
  lhs, rhs = batched_args
  lbd, rbd = batch_dims
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  left_stack_dim = lbd.stacked_axis if type(lbd) is RaggedAxis else lbd
  right_stack_dim = rbd.stacked_axis if type(rbd) is RaggedAxis else rbd
  new_dimension_numbers, result_stack_dim = _dot_general_batch_dim_nums(
      (np.ndim(lhs), np.ndim(rhs)), (left_stack_dim, right_stack_dim),
      dimension_numbers)
  # TODO Should probably check that any ragged dimensions have corresponding
  # sizes, because otherwise the dot product is technically undefined.
  #
  # This masking is not strictly necessary for non-contraction dimensions;
  # we could micro-optimize here by avoiding computing that mask.
  if type(lbd) is RaggedAxis:
    lhs = batching.mask_ragged_axes(lhs, _get_sum_identity, lbd)
    lhs_shape = batching.bdim_as_shape(lbd, lhs.shape)
  else:
    lhs_shape = np.shape(lhs)
  if type(rbd) is RaggedAxis:
    rhs = batching.mask_ragged_axes(rhs, _get_sum_identity, rbd)
    rhs_shape = batching.bdim_as_shape(rbd, rhs.shape)
  else:
    rhs_shape = np.shape(rhs)
  batched_out = dot_general(lhs, rhs, new_dimension_numbers,
                            precision=precision,
                            preferred_element_type=preferred_element_type)
  result_batch_dim = batching.shape_as_bdim(
      result_stack_dim,
      _dot_general_shape_computation(lhs_shape, rhs_shape, new_dimension_numbers))
  return batched_out, result_batch_dim
