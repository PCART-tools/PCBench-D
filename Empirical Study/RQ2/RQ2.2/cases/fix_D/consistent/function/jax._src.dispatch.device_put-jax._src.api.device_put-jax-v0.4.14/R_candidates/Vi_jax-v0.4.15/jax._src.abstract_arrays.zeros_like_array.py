def zeros_like_array(x):
  dtype, weak_type = dtypes._lattice_result_type(x)
  dtype = dtypes.canonicalize_dtype(dtype)
  aval = ShapedArray(np.shape(x), dtype, weak_type=weak_type)
  return ad_util.zeros_like_aval(aval)
