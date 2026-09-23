def _rng_uniform_lowering(ctx, a, b, *, shape):
  aval_out, = ctx.avals_out
  shape, = mlir.ir_constants(np.array(aval_out.shape, np.int64),
                             canonicalize_types=False)
  if jax._src.lib.mlir_api_version <= 22:
    return mhlo.RngUniformOp(a, b, shape).results
  else:
    return mhlo.RngOp(a, b, shape,
                      mhlo.RngDistributionAttr.get('UNIFORM')).results
