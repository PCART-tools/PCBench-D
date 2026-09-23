def _zeros_like_python_scalar(t, x):
  dtype = dtypes.canonicalize_dtype(dtypes.python_scalar_dtypes[t])
  aval = core.ShapedArray((), dtype, weak_type=True)
  return ad_util.zeros_like_aval(aval)
