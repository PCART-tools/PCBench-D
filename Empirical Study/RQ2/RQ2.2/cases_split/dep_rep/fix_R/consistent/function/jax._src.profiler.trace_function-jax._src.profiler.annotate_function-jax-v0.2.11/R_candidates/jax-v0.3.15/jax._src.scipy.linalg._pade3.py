def _pade3(A):
  b = (120., 60., 12., 1.)
  ident = jnp.eye(*A.shape, dtype=A.dtype)
  A2 = _precise_dot(A, A)
  U = _precise_dot(A, (b[3]*A2 + b[1]*ident))
  V = b[2]*A2 + b[0]*ident
  return U, V
