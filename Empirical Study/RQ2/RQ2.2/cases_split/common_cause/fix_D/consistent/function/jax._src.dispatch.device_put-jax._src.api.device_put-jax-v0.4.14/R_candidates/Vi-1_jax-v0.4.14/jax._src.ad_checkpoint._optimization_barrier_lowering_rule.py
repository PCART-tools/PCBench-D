def _optimization_barrier_lowering_rule(ctx, *args):
  barrier_types = map(mlir.aval_to_ir_types, ctx.avals_in)
  flat_args = mlir.flatten_lowering_ir_args(args)
  barrier_op = hlo.OptimizationBarrierOp(flat_args)
  return util.unflatten(barrier_op.results, map(len, barrier_types))
