def check_user_dtype_supported(dtype, fun_name=None):
  # Avoid using `dtype in [...]` because of numpy dtype equality overloading.
  if isinstance(dtype, type) and dtype in {bool, int, float, builtins.complex}:
    return
  np_dtype = np.dtype(dtype)
  is_custom_dtype = np_dtype.type in [float8_e4m3fn, float8_e5m2, bfloat16]
  if np_dtype.kind not in "biufc" and not is_custom_dtype:
    msg = f"JAX only supports number and bool dtypes, got dtype {dtype}"
    msg += f" in {fun_name}" if fun_name else ""
    raise TypeError(msg)
  if dtype is not None and np_dtype != canonicalize_dtype(dtype):
    msg = ("Explicitly requested dtype {} {} is not available, "
           "and will be truncated to dtype {}. To enable more dtypes, set the "
           "jax_enable_x64 configuration option or the JAX_ENABLE_X64 shell "
           "environment variable. "
           "See https://github.com/google/jax#current-gotchas for more.")
    fun_name = f"requested in {fun_name}" if fun_name else ""
    truncated_dtype = canonicalize_dtype(dtype).name
    warnings.warn(msg.format(dtype, fun_name , truncated_dtype), stacklevel=3)
