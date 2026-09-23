def zeros_like_lowering(ctx, x):
  aval, = ctx.avals_in
  assert isinstance(aval, core.ShapedArray), aval
  return [full_like_aval(ctx, 0, aval)]
