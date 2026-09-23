def qr_jvp_rule(primals, tangents, *, full_matrices):
  # See j-towns.github.io/papers/qr-derivative.pdf for a terse derivation.
  x, = primals
  dx, = tangents
  q, r = qr_p.bind(x, full_matrices=False)
  *_, m, n = x.shape
  if m < n or (full_matrices and m != n):
    raise NotImplementedError(
      "Unimplemented case of QR decomposition derivative")
  dx_rinv = triangular_solve(r, dx)  # Right side solve by default
  qt_dx_rinv = jnp.matmul(_H(q), dx_rinv)
  qt_dx_rinv_lower = jnp.tril(qt_dx_rinv, -1)
  do = qt_dx_rinv_lower - _H(qt_dx_rinv_lower)  # This is skew-symmetric
  # The following correction is necessary for complex inputs
  I = lax.expand_dims(jnp.eye(n, dtype=do.dtype), range(qt_dx_rinv.ndim - 2))
  do = do + I * (qt_dx_rinv - qt_dx_rinv.real.astype(qt_dx_rinv.dtype))
  dq = jnp.matmul(q, do - qt_dx_rinv) + dx_rinv
  dr = jnp.matmul(qt_dx_rinv - do, r)
  return (q, r), (dq, dr)
