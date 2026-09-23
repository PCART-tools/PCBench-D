def canonical_concrete_aval(val, weak_type=None):
  return ConcreteArray(dtypes.canonicalize_dtype(np.result_type(val)), val,
                       weak_type=weak_type)
