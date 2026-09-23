def _dot_general_batch_rule(batched_args, batch_dims, *, dimension_numbers,
                            precision,
                            preferred_element_type: Optional[DType]):
  lhs, rhs = batched_args
  new_dimension_numbers, result_batch_dim = _dot_general_batch_dim_nums(
      (lhs.ndim, rhs.ndim), batch_dims, dimension_numbers)
  batched_out = dot_general(lhs, rhs, new_dimension_numbers,
                            precision=precision,
                            preferred_element_type=preferred_element_type)
  return batched_out, result_batch_dim
