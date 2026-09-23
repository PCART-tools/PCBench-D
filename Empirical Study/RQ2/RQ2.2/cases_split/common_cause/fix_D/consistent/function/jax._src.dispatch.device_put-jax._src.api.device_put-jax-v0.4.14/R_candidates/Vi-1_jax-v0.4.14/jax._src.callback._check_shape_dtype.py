def _check_shape_dtype(shape_dtype):
  dt = np.dtype(shape_dtype.dtype)
  if dtypes.canonicalize_dtype(dt) != dt:
    raise ValueError(
        "Cannot return 64-bit values when `jax_enable_x64` is disabled")
