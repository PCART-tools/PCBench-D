def random_bits_lowering(ctx, keys, *, bit_width, shape):
  aval, = ctx.avals_in
  impl = aval.dtype.impl
  bits = iterated_vmap_unary(
      aval.ndim, lambda k: impl.random_bits(k, bit_width, shape))
  bits_lowering = mlir.lower_fun(bits, multiple_results=False)
  ctx_new = ctx.replace(avals_in=[keys_aval_to_base_arr_aval(aval)])
  out = bits_lowering(ctx_new, keys)
  ctx.set_tokens_out(ctx_new.tokens_out)
  return out
