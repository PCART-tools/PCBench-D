def _cond_lowering_rule(
    ctx: TritonLoweringRuleContext,
    index,
    *args,  # *consts, *ops
    branches,  # tuple(jaxprs)
    linear,
):
  block_infos = ctx.block_infos

  def to_type(out_aval):
    elt_type = _convert_dtype(out_aval.dtype)
    if not out_aval.shape:
      # Scalar types get special handling.
      return elt_type
    return tc.block_type(elt_type, out_aval.shape)

  out_types = [to_type(out) for out in ctx.avals_out]
  out_ir_types = [t.to_ir(ctx.builder) for t in out_types]

  use_branch0 = tc.semantic.equal(index, tc._to_tensor(0, index.dtype))
  # TODO(bjp): Switch to scf.index_switch once exposed in triton.cc
  if_op = scf_dialect.IfOp(use_branch0.handle, out_ir_types, hasElse=True)
  with ir.InsertionPoint.at_block_begin(if_op.then_block):
    outs0 = lower_jaxpr_to_triton_ir(
        ctx.context,
        branches[0].jaxpr,
        block_infos[1:],
        *args)
    scf_dialect.yield_([out.handle for out in outs0])
  with ir.InsertionPoint.at_block_begin(if_op.else_block):
    # TODO(bjp): Instead of linear nest of 'if's, partition into halves.
    if len(branches) > 2:
      outs1 = _cond_lowering_rule(
          ctx,
          tc.semantic.sub(index, tc._to_tensor(1, index.dtype)),
          *args,
          branches=branches[1:],
          linear=linear,
      )
    else:
      outs1 = lower_jaxpr_to_triton_ir(
          ctx.context,
          branches[1].jaxpr,
          block_infos[1:],
          *args)
    scf_dialect.yield_([out.handle for out in outs1])

  return map(tc.tensor, if_op.results_, out_types)
