def _custom_lin_transpose(cts_out, *invals, num_res, bwd, out_avals,
                          symbolic_zeros):
  res, _ = split_list(invals, [num_res])
  if symbolic_zeros:
    cts_out = map(replace_internal_symbolic_zeros, cts_out)
  else:
    cts_out = map(instantiate_zeros, cts_out)
  cts_in = bwd(*res, *cts_out)
  cts_in = map(replace_rule_output_symbolic_zeros, cts_in)
  return [None] * num_res + list(cts_in)
