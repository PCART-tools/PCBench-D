def _scan_lowering_rule(
    ctx: TritonLoweringRuleContext,
    *args,
    jaxpr,
    linear,
    length,
    reverse,
    unroll,
    num_consts,
    num_carry,
):
  # Only implements fori_loop-like scans
  num_extensive = len(args) - num_consts - num_carry
  if num_extensive: raise NotImplementedError
  if reverse: raise NotImplementedError
  if unroll != 1: raise NotImplementedError
  del linear, num_extensive, unroll, reverse

  builder = ctx.builder
  jaxpr, jaxpr_consts = jaxpr.jaxpr, jaxpr.consts
  if jaxpr_consts: raise NotImplementedError
  del jaxpr_consts

  jaxpr, has_loop_index = (
      pallas_utils.pattern_match_scan_to_fori_loop(jaxpr, num_consts, num_carry)
      )
  consts, args = util.split_list(args, [num_consts])
  if has_loop_index:
    lb, *args = args
    lower_bound = lb.handle
    ub = lb.__add__(tl.constexpr(length), _builder=builder)
    upper_bound = ub.handle
    bound_type = ub.type
  else:
    lower_bound = builder.get_int32(0)
    upper_bound = builder.get_int32(length)
    bound_type = tl.int32
  for_out = _lower_jaxpr_to_for_loop(
      ctx, jaxpr, lower_bound, upper_bound, consts, *args,
      has_loop_index=has_loop_index, step=1, bound_type=bound_type)
  if has_loop_index:
    # Need to return the final loop index value if the outer scan expects
    # it as an output
    return [tl.core.tensor(upper_bound, bound_type), *for_out]
  return for_out
