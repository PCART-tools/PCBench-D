def _dtype_to_xla_type_string(dtype: np.dtype) -> str:
  if dtype not in _dtype_to_xla_type_string_map:
    raise NotImplementedError(dtype)
  return _dtype_to_xla_type_string_map[dtype]
