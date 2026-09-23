@util._wraps(np.identity)
def identity(n: DimSize, dtype: DTypeLike | None = None) -> Array:
  dtypes.check_user_dtype_supported(dtype, "identity")
  return eye(n, dtype=dtype)
