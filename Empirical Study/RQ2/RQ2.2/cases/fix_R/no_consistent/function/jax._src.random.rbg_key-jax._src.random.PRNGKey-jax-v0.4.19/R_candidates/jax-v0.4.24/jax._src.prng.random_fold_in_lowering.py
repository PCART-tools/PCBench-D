def random_fold_in_lowering(ctx, keys, msgs):
  keys_aval, msgs_aval = ctx.avals_in
  impl = keys_aval.dtype._impl
  fold_in = iterated_vmap_binary_bcast(
      keys_aval.shape, msgs_aval.shape, impl.fold_in)
  fold_in_lowering = mlir.lower_fun(fold_in, multiple_results=False)
  return mlir.delegate_lowering(
      ctx, fold_in_lowering, keys, msgs,
      avals_in=[core.physical_aval(keys_aval), msgs_aval],
      avals_out=map(core.physical_aval, ctx.avals_out))
