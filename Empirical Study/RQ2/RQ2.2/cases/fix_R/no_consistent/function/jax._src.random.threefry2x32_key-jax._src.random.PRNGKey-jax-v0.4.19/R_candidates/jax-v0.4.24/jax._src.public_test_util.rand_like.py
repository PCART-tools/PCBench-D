def rand_like(rng, x):
  shape = np.shape(x)
  dtype = _dtype(x)
  randn = lambda: np.asarray(rng.randn(*shape), dtype=dtype)
  if _dtypes.issubdtype(dtype, np.complexfloating):
    result = randn() + dtype.type(1.0j) * randn()
  else:
    result = randn()
  return result.item() if is_python_scalar(x) else result
