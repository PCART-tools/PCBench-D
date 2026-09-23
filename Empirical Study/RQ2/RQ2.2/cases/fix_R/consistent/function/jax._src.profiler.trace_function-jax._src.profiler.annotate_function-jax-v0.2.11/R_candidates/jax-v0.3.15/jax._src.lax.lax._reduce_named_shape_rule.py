def _reduce_named_shape_rule(*avals, computation, jaxpr, consts, dimensions):
  # TODO(mattjj,frostig): see the TODOs noting limitations/assumptions in
  # _reduce_batching_rule. We're making the same assumptions here for now.
  num_operands = len(avals) // 2
  operand_avals, init_avals = split_list(avals, [num_operands])
  if any(a.named_shape for a in init_avals):
    raise NotImplementedError
  named_shapes = [a.named_shape for a in operand_avals]
  join = core.join_named_shapes(*(a.named_shape for a in operand_avals))
  return [join] * len(named_shapes)
