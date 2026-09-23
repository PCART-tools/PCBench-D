def make_shaped_array(x):
  dtype = dtypes.canonicalize_dtype(dtypes.result_type(x))
  return ShapedArray(np.shape(x), dtype)
