def _gather_pad_rule(in_avals, out_avals, operand, indices, *,
                     dimension_numbers, slice_sizes, unique_indices,
                     indices_are_sorted, mode, fill_value):
  operand_aval, indices_aval = in_avals
  if any(isinstance(d, pe.BoundedAxisSize) for d in operand_aval.shape):
    raise NotImplementedError
  if mode != GatherScatterMode.PROMISE_IN_BOUNDS:
    # with fill, jnp.where on operand; with clip, jnp.where on indices
    raise NotImplementedError
  return [gather(operand, indices, dimension_numbers=dimension_numbers,
                 slice_sizes=slice_sizes, mode=mode, fill_value=fill_value)]
