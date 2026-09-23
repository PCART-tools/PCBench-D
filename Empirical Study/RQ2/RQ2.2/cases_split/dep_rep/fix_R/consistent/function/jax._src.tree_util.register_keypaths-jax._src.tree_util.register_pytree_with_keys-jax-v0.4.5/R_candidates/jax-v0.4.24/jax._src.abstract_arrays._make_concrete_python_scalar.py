def _make_concrete_python_scalar(t, x):
  dtype = dtypes._scalar_type_to_dtype(t, x)
  weak_type = dtypes.is_weakly_typed(x)
  return canonical_concrete_aval(np.array(x, dtype=dtype), weak_type=weak_type)
