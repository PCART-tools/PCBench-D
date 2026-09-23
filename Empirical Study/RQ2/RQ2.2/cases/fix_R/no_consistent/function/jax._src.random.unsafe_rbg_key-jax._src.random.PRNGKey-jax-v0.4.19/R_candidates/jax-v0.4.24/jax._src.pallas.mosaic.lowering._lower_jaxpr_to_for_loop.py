def _lower_jaxpr_to_for_loop(ctx: LoweringRuleContext,
                             jaxpr: jax_core.Jaxpr, start: int,
                             num_steps: int, consts, *args,
                             has_loop_index: bool,
                             unroll: int):
  def _run_body(i, args):
    if has_loop_index:
      lowering_context = ctx.lowering_context.replace(
          block_shapes=ctx.block_shapes)
      args = jaxpr_subcomp(lowering_context, jaxpr, *consts, i, *args)
    else:
      del i
      lowering_context = ctx.lowering_context.replace(
          block_shapes=ctx.block_shapes[:len(consts)]
          + ctx.block_shapes[len(consts) + 1:],
      )
      args = jaxpr_subcomp(lowering_context, jaxpr, *consts, *args)
    return args

  if num_steps == unroll:
    # No need for an scf.For. We can just unroll completely
    for i in range(start, start + num_steps):
      args = _run_body(
          ir_constant(i, mlir_type=_dtype_to_ir_type(jnp.dtype("int32"))),
          args,
      )
    return args
  if unroll != 1:
    raise NotImplementedError(
        f"Only unroll={num_steps=} and unroll=1 supported. Got {unroll=}.")
  lbd = ir_constant(0, mlir_type=mlir.dtype_to_ir_type(jnp.dtype("int32")))
  ubd = ir_constant(
      num_steps, mlir_type=_dtype_to_ir_type(jnp.dtype("int32"))
  )
  step = ir_constant(1, mlir_type=_dtype_to_ir_type(jnp.dtype("int32")))
  for_op = scf.ForOp(lbd, ubd, step, args)
  with ir.InsertionPoint(for_op.body):
    iv = for_op.induction_variable
    inner_args = for_op.inner_iter_args
    inner_out = _run_body(iv, inner_args)
    scf.YieldOp(inner_out)
  return for_op.results
