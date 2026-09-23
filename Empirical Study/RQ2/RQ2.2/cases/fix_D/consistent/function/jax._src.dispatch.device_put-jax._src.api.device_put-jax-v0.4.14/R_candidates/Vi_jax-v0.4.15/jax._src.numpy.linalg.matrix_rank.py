@_wraps(np.linalg.matrix_rank)
@jit
def matrix_rank(M: ArrayLike, tol: Optional[ArrayLike] = None) -> Array:
  check_arraylike("jnp.linalg.matrix_rank", M)
  M, = promote_dtypes_inexact(jnp.asarray(M))
  if M.ndim < 2:
    return (M != 0).any().astype(jnp.int32)
  S = svd(M, full_matrices=False, compute_uv=False)
  if tol is None:
    tol = S.max(-1) * np.max(M.shape[-2:]).astype(S.dtype) * jnp.finfo(S.dtype).eps
  tol = jnp.expand_dims(tol, np.ndim(tol))
  return reductions.sum(S > tol, axis=-1)
