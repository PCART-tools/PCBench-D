def _make_concrete_python_scalar(t, x):
  dtype = dtypes._scalar_type_to_dtype(t, x)
  return canonical_concrete_aval(np.array(x, dtype=dtype), weak_type=True)
