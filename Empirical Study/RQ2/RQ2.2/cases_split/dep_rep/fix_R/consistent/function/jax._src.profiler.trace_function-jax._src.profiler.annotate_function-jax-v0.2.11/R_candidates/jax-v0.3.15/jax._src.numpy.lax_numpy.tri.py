@_wraps(np.tri)
def tri(N, M=None, k=0, dtype=None):
  lax_internal._check_user_dtype_supported(dtype, "tri")
  M = M if M is not None else N
  dtype = dtype or float32
  return lax_internal._tri(dtype, (N, M), k)
