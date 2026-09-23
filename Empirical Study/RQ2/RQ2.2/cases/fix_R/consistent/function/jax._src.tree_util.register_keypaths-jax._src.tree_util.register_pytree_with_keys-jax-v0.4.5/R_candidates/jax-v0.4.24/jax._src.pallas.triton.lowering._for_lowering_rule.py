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
  lower_bound = _i32_constant(0)
  upper_bound = _i32_constant(nsteps)
  step = _i32_constant(1)
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
  for_op = scf_dialect.ForOp(
      lower_bound, upper_bound, step, [arg.handle for arg in loop_args]
  )
  with ir.InsertionPoint(for_op.body):
    loop_index = tc.tensor(for_op.induction_variable, tc.int32)
    # Emit loop body
    for_body_args = [
        tc.tensor(for_op.body.arguments[i + 1], arg.type)
        for i, arg in enumerate(loop_args)
    ]
    loop_body_args = merge_lists(is_loop_arg, non_loop_args, for_body_args)
    out_discharged = lower_jaxpr_to_triton_ir(
        ctx.context,
        discharged_jaxpr,
        [None, *ctx.block_infos],
        loop_index,
        *loop_body_args,
    )
    all_out = merge_lists(should_discharge, ptrs, out_discharged)
    _, loop_out = partition_list(is_loop_arg, all_out)
    scf_dialect.yield_([arg.handle for arg in loop_out])
  for_out = [tc.tensor(r, a.type) for r, a in zip(for_op.results_, loop_args)]
  return merge_lists(is_loop_arg, non_loop_args, for_out)
