def _slogdet_jvp(primals, tangents):
  x, = primals
  g, = tangents
  sign, ans = slogdet(x)
  ans_dot = jnp.trace(solve(x, g), axis1=-1, axis2=-2)
  if jnp.issubdtype(jnp._dtype(x), jnp.complexfloating):
    sign_dot = (ans_dot - jnp.real(ans_dot).astype(ans_dot.dtype)) * sign
    ans_dot = jnp.real(ans_dot)
  else:
    sign_dot = jnp.zeros_like(sign)
  return (sign, ans), (sign_dot, ans_dot)
