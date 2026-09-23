def _lower_jaxpr_to_for_loop(ctx: TritonLoweringRuleContext, jaxpr: jax_core.Jaxpr,
                             lower_bound, upper_bound, consts, *args,
                             has_loop_index: bool,
                             step: int = 1,
                             bound_type: tl.dtype = tl.int32):
  if step != 1:
    raise NotImplementedError
  builder = ctx.builder
  if bound_type == tl.int64:
    step = builder.get_int64(step)
  else:
    step = builder.get_int32(step)
  current_block = builder.get_insertion_block()
  for_op = builder.create_for_op(
      lower_bound, upper_bound, step, [arg.handle for arg in args]
  )
  loop_block = builder.create_block()
  builder.set_insertion_point_to_start(loop_block)
  loop_index = tl.core.tensor(for_op.get_induction_var(), tl.core.int32)
  # Emit loop body
  for_body_args = [
      tl.core.tensor(for_op.get_body(0).arg(i + 1), arg.type)
      for i, arg in enumerate(args)
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
  if all_out:
    builder.create_yield_op([arg.handle for arg in all_out])
  loop_block.merge_block_before(for_op.get_body(0))
  for_results = [for_op.get_result(i) for i in range(len(args))]
  builder.set_insertion_point_to_end(current_block)
  return [tl.core.tensor(r, a.type) for r, a in zip(for_results, args)]
