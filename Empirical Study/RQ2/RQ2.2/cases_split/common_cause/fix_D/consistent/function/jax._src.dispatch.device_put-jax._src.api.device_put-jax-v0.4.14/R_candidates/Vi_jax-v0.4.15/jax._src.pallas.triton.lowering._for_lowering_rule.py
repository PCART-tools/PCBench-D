def _for_lowering_rule(
    ctx: TritonLoweringRuleContext,
    *args,
    jaxpr,
    which_linear,
    nsteps,
    reverse,
    unroll
):
  del which_linear
  if reverse or unroll != 1:
    raise NotImplementedError
  builder = ctx.builder
  lower_bound = builder.get_int32(0)
  upper_bound = builder.get_int32(nsteps)
  step = builder.get_int32(1)
  current_block = builder.get_insertion_block()
  init_args = args
  # Partially discharge state from jaxpr for non-pointers
  should_discharge = [not isinstance(a, AbstractRef) for a in ctx.avals_in]
  discharged_jaxpr, () = discharge.discharge_state(
      jaxpr, (), should_discharge=[True, *should_discharge]
  )
  in_avals = [v.aval for v in jaxpr.invars]
  state_effects = state.get_ref_state_effects(in_avals, jaxpr.effects)[1:]
  # Read-only `Ref`s don't need to be passed in explicitly as loop arguments so
  # we can filter them out.
  read_only = map(_is_read_only, state_effects)
  is_loop_arg = map(
      operator.and_, map(operator.not_, read_only), should_discharge
  )
  ptrs, _ = partition_list(should_discharge, init_args)
  non_loop_args, loop_args = partition_list(is_loop_arg, init_args)
  for_op = builder.create_for_op(
      lower_bound, upper_bound, step, [arg.handle for arg in loop_args]
  )
  loop_block = builder.create_block()
  builder.set_insertion_point_to_start(loop_block)
  loop_index = tl.core.tensor(for_op.get_induction_var(), tl.core.int32)
  # Emit loop body
  for_body_args = [
      tl.core.tensor(for_op.get_body(0).arg(i + 1), arg.type)
      for i, arg in enumerate(loop_args)
  ]
  loop_body_args = merge_lists(is_loop_arg, non_loop_args, for_body_args)
  out_discharged = lower_jaxpr_to_triton_ir(
      ctx.context,
      discharged_jaxpr,
      [None, *ctx.block_infos],
      loop_index,
      *loop_body_args
  )
  all_out = merge_lists(should_discharge, ptrs, out_discharged)
  _, loop_out = partition_list(is_loop_arg, all_out)
  if loop_out:
    builder.create_yield_op([arg.handle for arg in loop_out])
  loop_block.merge_block_before(for_op.get_body(0))
  for_results = [for_op.get_result(i) for i in range(len(loop_args))]
  builder.set_insertion_point_to_end(current_block)
  for_out = [tl.core.tensor(r, a.type) for r, a in zip(for_results, loop_args)]
  return merge_lists(is_loop_arg, non_loop_args, for_out)
