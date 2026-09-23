@util._wraps(np.eye)
def eye(N: DimSize, M: Optional[DimSize] = None, k: int = 0,
        dtype: Optional[DTypeLike] = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "eye")
  N_int = core.canonicalize_dim(N, "'N' argument of jnp.eye()")
  M_int = N_int if M is None else core.canonicalize_dim(M, "'M' argument of jnp.eye()")
  if N_int < 0 or M_int < 0:
    raise ValueError(f"negative dimensions are not allowed, got {N} and {M}")
  k = operator.index(k)
  return lax_internal._eye(_jnp_dtype(dtype), (N_int, M_int), k)
