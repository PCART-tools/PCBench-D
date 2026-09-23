def _numpy_array_abstractify(x: np.ndarray) -> ShapedArray:
  dtype = x.dtype
  dtypes.check_valid_dtype(dtype)
  return ShapedArray(x.shape,
      dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True))
