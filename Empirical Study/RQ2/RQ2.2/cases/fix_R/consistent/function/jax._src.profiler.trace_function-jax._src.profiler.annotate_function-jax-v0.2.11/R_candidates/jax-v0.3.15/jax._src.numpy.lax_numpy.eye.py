@_wraps(np.eye)
def eye(N, M=None, k=0, dtype=None):
  lax_internal._check_user_dtype_supported(dtype, "eye")
  N = core.canonicalize_dim(N, "'N' argument of jnp.eye()")
  M = N if M is None else core.canonicalize_dim(M, "'M' argument of jnp.eye()")
  if N < 0 or M < 0:
    raise ValueError(f"negative dimensions are not allowed, got {N} and {M}")
  k = operator.index(k)
  return lax_internal._eye(_jnp_dtype(dtype), (N, M), k)
