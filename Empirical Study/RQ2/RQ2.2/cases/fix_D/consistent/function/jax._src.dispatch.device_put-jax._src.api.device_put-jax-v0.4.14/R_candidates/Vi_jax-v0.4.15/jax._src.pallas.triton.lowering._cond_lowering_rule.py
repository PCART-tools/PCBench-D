def _cond_lowering_rule(
    ctx: TritonLoweringRuleContext,
    index,
    *args,  # *consts, *ops
    branches,  # tuple(jaxprs)
    linear,
):
  block_infos = ctx.block_infos
  current_bb = ctx.builder.get_insertion_block()

  def to_type(out_aval):
    elt_type = code_gen.str_to_ty(get_triton_type(out_aval)).element_ty
    if not out_aval.shape:
      # Scalar types get special handling.
      return elt_type
    return tl.block_type(elt_type, out_aval.shape)

  out_types = [to_type(out) for out in ctx.avals_out]
  out_ir_types = [t.to_ir(ctx.builder) for t in out_types]

  use_branch0 = index.__eq__(0, _builder=ctx.builder)
  # TODO(bjp): Switch to scf.index_switch once exposed in triton.cc
  if_op = ctx.builder.create_if_op(
      out_ir_types,  # retTypes
      use_branch0.handle,  # condition
      True)  # withElse
  # Lower then block.
  ctx.builder.set_insertion_point_to_start(if_op.get_then_block())
  outs0 = lower_jaxpr_to_triton_ir(
      ctx.context,
      branches[0].jaxpr,
      block_infos[1:],
      *args)
  if outs0:
    ctx.builder.create_yield_op([out.handle for out in outs0])
  # Lower else block.
  ctx.builder.set_insertion_point_to_start(if_op.get_else_block())
  # TODO(bjp): Instead of linear nest of 'if's, partition into halves.
  if len(branches) > 2:
    outs1 = _cond_lowering_rule(
        ctx,
        index.__sub__(1, _builder=ctx.builder),
        *args,
        branches=branches[1:],
        linear=linear)
  else:
    outs1 = lower_jaxpr_to_triton_ir(
        ctx.context,
        branches[1].jaxpr,
        block_infos[1:],
        *args)
  if outs1:
    ctx.builder.create_yield_op([out.handle for out in outs1])
  ctx.builder.set_insertion_point_to_end(current_bb)
  all_out = [
      tl.core.tensor(if_op.get_result(i), ty)
      for i, ty in enumerate(out_types)
  ]
  return all_out
