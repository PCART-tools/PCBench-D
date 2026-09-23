def _check_user_dtype_supported(dtype, fun_name=None):
  # Avoid using `dtype in [...]` because of numpy dtype equality overloading.
  if isinstance(dtype, type) and dtype in {bool, int, float, builtins.complex}:
    return
  np_dtype = np.dtype(dtype)
  if np_dtype.kind not in "biufc" and np_dtype.type != dtypes.bfloat16:
    msg = f"JAX only supports number and bool dtypes, got dtype {dtype}"
    msg += f" in {fun_name}" if fun_name else ""
    raise TypeError(msg)
  if dtype is not None and np_dtype != dtypes.canonicalize_dtype(dtype):
    msg = ("Explicitly requested dtype {} {} is not available, "
           "and will be truncated to dtype {}. To enable more dtypes, set the "
           "jax_enable_x64 configuration option or the JAX_ENABLE_X64 shell "
           "environment variable. "
           "See https://github.com/google/jax#current-gotchas for more.")
    fun_name = f"requested in {fun_name}" if fun_name else ""
    truncated_dtype = dtypes.canonicalize_dtype(dtype).name
    warnings.warn(msg.format(dtype, fun_name , truncated_dtype), stacklevel=3)
