def random_split_lowering(ctx, keys, *, count):
  aval, = ctx.avals_in
  impl = aval.dtype.impl
  split = iterated_vmap_unary(aval.ndim, lambda k: impl.split(k, count))
  split_lowering = mlir.lower_fun(split, multiple_results=False)
  return mlir.delegate_lowering(
      ctx, split_lowering, keys,
      avals_in=[keys_aval_to_base_arr_aval(aval)],
      avals_out=map(keys_aval_to_base_arr_aval, ctx.avals_out))
