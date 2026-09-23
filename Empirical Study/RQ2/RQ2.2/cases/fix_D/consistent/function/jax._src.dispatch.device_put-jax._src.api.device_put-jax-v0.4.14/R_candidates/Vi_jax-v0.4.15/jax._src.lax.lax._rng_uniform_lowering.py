def _rng_uniform_lowering(ctx, a, b, *, shape):
  aval_out, = ctx.avals_out
  shape, = mlir.ir_constants(np.array(aval_out.shape, np.int64))
  return hlo.RngOp(a, b, shape,
                   hlo.RngDistributionAttr.get('UNIFORM')).results
