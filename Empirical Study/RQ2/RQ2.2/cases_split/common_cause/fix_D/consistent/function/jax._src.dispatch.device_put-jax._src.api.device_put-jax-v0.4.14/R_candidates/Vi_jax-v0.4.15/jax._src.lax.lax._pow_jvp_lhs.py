def _pow_jvp_lhs(g, ans, x, y):
  y_dtype = dtypes.dtype(y)
  x, y = jax._src.numpy.util.promote_dtypes_numeric(x, y)  # TODO replace this
  if dtypes.issubdtype(y_dtype, np.integer):
    if x.shape != y.shape:
      shape = broadcast_shapes(x.shape, y.shape)
      x = _maybe_broadcast(shape, x)
      y = _maybe_broadcast(shape, y)
    jac = select(eq(y, _const(y, 0)), _ones(y),
                 mul(_replace_zero(y), pow(x, sub(y, _ones(y)))))
  else:
    jac = mul(y, pow(x, sub(y, _ones(y))))
  return mul(g, jac)
