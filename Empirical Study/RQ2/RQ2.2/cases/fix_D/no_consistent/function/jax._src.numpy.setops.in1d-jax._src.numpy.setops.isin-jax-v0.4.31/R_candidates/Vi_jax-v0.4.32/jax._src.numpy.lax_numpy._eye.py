def _eye(N: DimSize, M: DimSize | None = None,
        k: int | ArrayLike = 0,
        dtype: DTypeLike | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "eye")
  if isinstance(k, int):
    k = lax_internal._clip_int_to_valid_range(k, np.int32,
                                              "`argument `k` of jax.numpy.eye")
  util.check_arraylike("eye", k)
  offset = asarray(k)
  if not (offset.shape == () and dtypes.issubdtype(offset.dtype, np.integer)):
    raise ValueError(f"k must be a scalar integer; got {k}")
  N_int = core.canonicalize_dim(N, "argument of 'N' jnp.eye()")
  M_int = N_int if M is None else core.canonicalize_dim(M, "argument 'M' of jnp.eye()")
  if N_int < 0 or M_int < 0:
    raise ValueError(f"negative dimensions are not allowed, got {N} and {M}")
  i = lax.broadcasted_iota(offset.dtype, (N_int, M_int), 0)
  j = lax.broadcasted_iota(offset.dtype, (N_int, M_int), 1)
  return (i + offset == j).astype(dtype)
