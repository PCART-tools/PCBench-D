def _dot_general_batch_rule(batched_args, batch_dims, *, dimension_numbers,
                            precision,
                            preferred_element_type: Optional[DTypeLike]):
  lhs, rhs = batched_args
  lbd, rbd = batch_dims
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  if (type(lbd) is type(rbd) is ConcatAxis and
      lbd.axis in lhs_contract and rbd.axis in rhs_contract):
    # first handle any other part of the dot with these as batch dims
    lhs_contract_ = [d for d in lhs_contract if d != lbd.axis]
    rhs_contract_ = [d for d in rhs_contract if d != rbd.axis]
    lhs_batch_ = (lbd.axis, *lhs_batch)
    rhs_batch_ = (rbd.axis, *rhs_batch)
    new_dnums = ((lhs_contract_, rhs_contract_), (lhs_batch_, rhs_batch_))
    out = dot_general(lhs, rhs, new_dnums, precision=precision,
                      preferred_element_type=preferred_element_type)
    # now a segment sum along that batch axis
    return batching.segment_sum(out, lbd.segment_lengths), 0

  new_dimension_numbers, result_batch_dim = _dot_general_batch_dim_nums(
      (lhs.ndim, rhs.ndim), batch_dims, dimension_numbers)
  batched_out = dot_general(lhs, rhs, new_dimension_numbers,
                            precision=precision,
                            preferred_element_type=preferred_element_type)
  return batched_out, result_batch_dim
