@_wraps(np.identity)
def identity(n, dtype=None):
  lax_internal._check_user_dtype_supported(dtype, "identity")
  return eye(n, dtype=dtype)
