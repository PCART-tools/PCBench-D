def _lower_jaxpr_to_for_loop(ctx: TritonLoweringRuleContext, jaxpr: jax_core.Jaxpr,
                             lower_bound, upper_bound, consts, *args,
                             has_loop_index: bool,
                             step: int = 1,
                             bound_type: tc.dtype = tc.int32):
  if step != 1:
    raise NotImplementedError
  if bound_type == tc.int64:
    step = _i64_constant(step)
  else:
    step = _i32_constant(step)

  for_op = scf_dialect.ForOp(
      lower_bound, upper_bound, step, [arg.handle for arg in args]
  )
  with ir.InsertionPoint.at_block_begin(for_op.body):
    loop_index = tc.tensor(for_op.induction_variable, bound_type)
    for_body_args = [
        tc.tensor(for_op.body.arguments[i + 1], arg.type) for i, arg in enumerate(args)
    ]
    if has_loop_index:
      jaxpr_args = [*consts, loop_index, *for_body_args]
    else:
      jaxpr_args = [*consts, *for_body_args]
    all_out = lower_jaxpr_to_triton_ir(
        ctx.context,
        jaxpr,
        ctx.block_infos,
        *jaxpr_args)
    scf_dialect.yield_([arg.handle for arg in all_out])

  return [tc.tensor(r, a.type) for r, a in zip(for_op.results_, args)]
