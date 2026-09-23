def _np_scalar_abstractify(x: np.generic) -> ShapedArray:
  dtype = np.dtype(x)
  dtypes.check_valid_dtype(dtype)
  return ShapedArray(np.shape(x),
      dtypes.canonicalize_dtype(dtype, allow_extended_dtype=True))
