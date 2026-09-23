def _possible_downcast(x, example):
  if (dtypes.issubdtype(x.dtype, np.complexfloating) and
      not dtypes.issubdtype(_dtype(example), np.complexfloating)):
    x = x.real
  dtype = None if example is None else _dtype(example)
  weak_type = None if example is None else dtypes.is_weakly_typed(example)
  return lax_internal._convert_element_type(x, dtype, weak_type)
