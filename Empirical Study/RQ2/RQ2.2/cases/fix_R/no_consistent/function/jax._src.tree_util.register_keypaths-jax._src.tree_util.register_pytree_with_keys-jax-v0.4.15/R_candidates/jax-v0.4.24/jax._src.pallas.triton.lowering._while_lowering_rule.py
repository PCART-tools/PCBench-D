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
  cond_consts, body_consts, carry = util.split_list(
      args, [cond_nconsts, body_nconsts]
  )
  cond_const_block_infos, body_const_block_infos, carry_block_infos = (
      util.split_list(ctx.block_infos, [cond_nconsts, body_nconsts])
  )
  cond_const_types = [a.type.to_ir(ctx.builder) for a in cond_consts]
  body_const_types = [a.type.to_ir(ctx.builder) for a in body_consts]
  carry_types = [a.type.to_ir(ctx.builder) for a in carry]
  all_types = [*cond_const_types, *body_const_types, *carry_types]
  while_op = scf_dialect.WhileOp(
      all_types,
      [arg.handle for arg in args],
  )

  before_block = while_op.before.blocks.append(*all_types)
  cond_consts_, _, carry_ = util.split_list(
      before_block.arguments,
      [cond_nconsts, body_nconsts],
  )
  cond_args = [
      tc.tensor(a, b.type)
      for a, b in zip([*cond_consts_, *carry_], [*cond_consts, *carry])
  ]
  with ir.InsertionPoint.at_block_begin(before_block):
    [cond] = lower_jaxpr_to_triton_ir(
        ctx.context,
        cond_jaxpr.jaxpr,
        [*cond_const_block_infos, *carry_block_infos],
        *cond_args,
    )
    scf_dialect.condition(cond.handle, before_block.arguments)

  after_block = while_op.after.blocks.append(*all_types)
  cond_consts_, body_consts_, carry_ = util.split_list(
      after_block.arguments,
      [cond_nconsts, body_nconsts],
  )
  all_args = [
      tc.tensor(a, b.type)
      for a, b in zip(
          [*cond_consts_, *body_consts_, *carry_],
          [*cond_consts, *body_consts, *carry],
      )
  ]
  cond_const_args, body_const_args, carry_args = util.split_list(
      all_args, [cond_nconsts, body_nconsts]
  )
  with ir.InsertionPoint.at_block_begin(after_block):
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
      scf_dialect.yield_(all_handles)

  all_out =  [
      tc.tensor(r, a.type) for r, a in zip(while_op.results_, args)
  ]
  return all_out[cond_nconsts + body_nconsts :]
