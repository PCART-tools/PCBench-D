def _svd_jvp_rule(primals, tangents, *, full_matrices, compute_uv):
  A, = primals
  dA, = tangents
  s, U, Vt = svd_p.bind(A, full_matrices=False, compute_uv=True)

  if compute_uv and full_matrices:
    # TODO: implement full matrices case, documented here: https://people.maths.ox.ac.uk/gilesm/files/NA-08-01.pdf
    raise NotImplementedError(
      "Singular value decomposition JVP not implemented for full matrices")

  Ut, V = _H(U), _H(Vt)
  s_dim = s[..., None, :]
  dS = jnp.matmul(jnp.matmul(Ut, dA), V)
  ds = jnp.real(jnp.diagonal(dS, 0, -2, -1))

  if not compute_uv:
    return (s,), (ds,)

  s_diffs = (s_dim + _T(s_dim)) * (s_dim - _T(s_dim))
  s_diffs_zeros = jnp.eye(s.shape[-1], dtype=s.dtype)  # jnp.ones((), dtype=A.dtype) * (s_diffs == 0.)  # is 1. where s_diffs is 0. and is 0. everywhere else
  s_diffs_zeros = lax.expand_dims(s_diffs_zeros, range(s_diffs.ndim - 2))
  F = 1 / (s_diffs + s_diffs_zeros) - s_diffs_zeros
  dSS = s_dim.astype(A.dtype) * dS  # dS.dot(jnp.diag(s))
  SdS = _T(s_dim.astype(A.dtype)) * dS  # jnp.diag(s).dot(dS)

  s_zeros = (s == 0).astype(s.dtype)
  s_inv = 1 / (s + s_zeros) - s_zeros
  s_inv_mat = jnp.vectorize(jnp.diag, signature='(k)->(k,k)')(s_inv)
  dUdV_diag = .5 * (dS - _H(dS)) * s_inv_mat.astype(A.dtype)
  dU = jnp.matmul(U, F.astype(A.dtype) * (dSS + _H(dSS)) + dUdV_diag)
  dV = jnp.matmul(V, F.astype(A.dtype) * (SdS + _H(SdS)))

  m, n = A.shape[-2:]
  if m > n:
    I = lax.expand_dims(jnp.eye(m, dtype=A.dtype), range(U.ndim - 2))
    dU = dU + jnp.matmul(I - jnp.matmul(U, Ut), jnp.matmul(dA, V)) / s_dim.astype(A.dtype)
  if n > m:
    I = lax.expand_dims(jnp.eye(n, dtype=A.dtype), range(V.ndim - 2))
    dV = dV + jnp.matmul(I - jnp.matmul(V, Vt), jnp.matmul(_H(dA), U)) / s_dim.astype(A.dtype)

  return (s, U, Vt), (ds, dU, _H(dV))
