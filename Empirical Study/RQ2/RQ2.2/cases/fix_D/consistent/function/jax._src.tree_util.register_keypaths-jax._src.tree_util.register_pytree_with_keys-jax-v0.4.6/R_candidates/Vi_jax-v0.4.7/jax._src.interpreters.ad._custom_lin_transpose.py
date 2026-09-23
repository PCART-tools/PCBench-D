def _custom_lin_transpose(cts_out, *invals, num_res, bwd, out_avals):
  res, _ = split_list(invals, [num_res])
  cts_out = map(instantiate_zeros_aval, out_avals, cts_out)
  cts_in = bwd(*res, *cts_out)
  return [None] * num_res + list(cts_in)
