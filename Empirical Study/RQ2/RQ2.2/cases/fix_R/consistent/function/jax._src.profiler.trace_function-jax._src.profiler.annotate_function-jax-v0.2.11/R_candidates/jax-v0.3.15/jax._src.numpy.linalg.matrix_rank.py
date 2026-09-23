@_wraps(np.linalg.matrix_rank)
@jit
def matrix_rank(M, tol=None):
  M, = _promote_dtypes_inexact(jnp.asarray(M))
  if M.ndim > 2:
    raise TypeError("array should have 2 or fewer dimensions")
  if M.ndim < 2:
    return jnp.any(M != 0).astype(jnp.int32)
  S = svd(M, full_matrices=False, compute_uv=False)
  if tol is None:
    tol = S.max() * np.max(M.shape).astype(S.dtype) * jnp.finfo(S.dtype).eps
  return jnp.sum(S > tol)
