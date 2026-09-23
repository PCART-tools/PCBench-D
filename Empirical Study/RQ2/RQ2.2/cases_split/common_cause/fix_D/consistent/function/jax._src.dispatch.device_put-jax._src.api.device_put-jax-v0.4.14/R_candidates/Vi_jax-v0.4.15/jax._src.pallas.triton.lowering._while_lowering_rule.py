def _while_lowering_rule(
    ctx: TritonLoweringRuleContext,
    *args,
    cond_nconsts,
    cond_jaxpr,
    body_nconsts,
    body_jaxpr
):
  # First, try to pattern match to fori_loop and lower to scf.for if possible
  result = _maybe_pattern_match_fori_loop(ctx, *args, cond_nconsts=cond_nconsts,
                                          body_nconsts=body_nconsts, cond_jaxpr=cond_jaxpr,
                                          body_jaxpr=body_jaxpr)
  if result is not None:
    return result
  # Fall back to default while lowering
  num_args = len(args)
  cond_consts, body_consts, carry = util.split_list(
      args, [cond_nconsts, body_nconsts]
  )
  cond_const_block_infos, body_const_block_infos, carry_block_infos = (
      util.split_list(ctx.block_infos, [cond_nconsts, body_nconsts])
  )
  current_bb = ctx.builder.get_insertion_block()
  cond_const_types = [a.type.to_ir(ctx.builder) for a in cond_consts]
  body_const_types = [a.type.to_ir(ctx.builder) for a in body_consts]
  carry_types = [a.type.to_ir(ctx.builder) for a in carry]
  all_types = [*cond_const_types, *body_const_types, *carry_types]
  while_op = ctx.builder.create_while_op(
      [*cond_const_types, *body_const_types, *carry_types],
      [arg.handle for arg in args],
  )
  before_block = ctx.builder.create_block_with_parent(
      while_op.get_before(), all_types
  )
  ctx.builder.set_insertion_point_to_start(before_block)
  cond_consts_, _, carry_ = util.split_list(
      [before_block.arg(i) for i in range(num_args)],
      [cond_nconsts, body_nconsts],
  )
  cond_args = [
      tl.core.tensor(a, b.type)
      for a, b in zip([*cond_consts_, *carry_], [*cond_consts, *carry])
  ]
  (cond,) = lower_jaxpr_to_triton_ir(
      ctx.context,
      cond_jaxpr.jaxpr,
      [*cond_const_block_infos, *carry_block_infos],
      *cond_args
  )
  ctx.builder.create_condition_op(
      cond.handle, [before_block.arg(i) for i in range(num_args)]
  )
  after_block = ctx.builder.create_block_with_parent(
      while_op.get_after(), all_types
  )
  ctx.builder.set_insertion_point_to_start(after_block)
  cond_consts_, body_consts_, carry_ = util.split_list(
      [after_block.arg(i) for i in range(num_args)],
      [cond_nconsts, body_nconsts],
  )
  all_args = [
      tl.core.tensor(a, b.type)
      for a, b in zip(
          [*cond_consts_, *body_consts_, *carry_],
          [*cond_consts, *body_consts, *carry],
      )
  ]
  cond_const_args, body_const_args, carry_args = util.split_list(
      all_args, [cond_nconsts, body_nconsts]
  )
  loop_out = lower_jaxpr_to_triton_ir(
      ctx.context,
      body_jaxpr.jaxpr,
      [*body_const_block_infos, *carry_block_infos],
      *body_const_args,
      *carry_args
  )
  cond_consts_handles = [a.handle for a in cond_const_args]
  body_consts_handles = [a.handle for a in body_const_args]
  loop_out_handles = [a.handle for a in loop_out]
  all_handles = [*cond_consts_handles, *body_consts_handles, *loop_out_handles]
  if all_handles:
    ctx.builder.create_yield_op(all_handles)
  ctx.builder.set_insertion_point_to_end(current_bb)
  all_out = [
      tl.core.tensor(while_op.get_result(i), a.type) for i, a in enumerate(args)
  ]
  return all_out[cond_nconsts + body_nconsts :]
