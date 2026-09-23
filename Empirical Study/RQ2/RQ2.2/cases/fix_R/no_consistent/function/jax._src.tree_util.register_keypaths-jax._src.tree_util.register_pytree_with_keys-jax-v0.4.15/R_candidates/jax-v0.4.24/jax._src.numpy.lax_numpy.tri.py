@util.implements(np.tri)
def tri(N: int, M: int | None = None, k: int = 0, dtype: DTypeLike | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "tri")
  M = M if M is not None else N
  dtype = dtype or float32
  return lax_internal._tri(dtype, (N, M), k)
