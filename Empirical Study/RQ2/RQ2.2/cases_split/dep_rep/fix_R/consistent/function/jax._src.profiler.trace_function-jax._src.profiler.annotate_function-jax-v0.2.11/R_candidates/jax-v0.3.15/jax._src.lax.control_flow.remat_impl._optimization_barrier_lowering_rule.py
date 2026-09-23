def _optimization_barrier_lowering_rule(ctx, *args):
  barrier_types = _map(mlir.aval_to_ir_types, ctx.avals_in)
  flat_barrier_types = util.flatten(barrier_types)

  flat_args = mlir.flatten_lowering_ir_args(args)
  barrier_op = mhlo.OptimizationBarrierOp(flat_barrier_types, flat_args)
  return util.unflatten(barrier_op.results, _map(len, barrier_types))
