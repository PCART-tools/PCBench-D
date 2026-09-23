def random_seed_lowering(ctx, seeds, *, impl):
  aval, = ctx.avals_in
  seed = iterated_vmap_unary(aval.ndim, impl.seed)
  seed_lowering = mlir.lower_fun(seed, multiple_results=False)
  return mlir.delegate_lowering(
      ctx, seed_lowering, seeds,
      avals_out=map(core.physical_aval, ctx.avals_out))
