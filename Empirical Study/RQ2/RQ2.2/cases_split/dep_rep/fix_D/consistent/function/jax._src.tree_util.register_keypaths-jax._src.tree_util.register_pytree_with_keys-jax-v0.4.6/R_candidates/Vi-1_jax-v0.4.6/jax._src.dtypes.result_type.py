def result_type(*args: Any, return_weak_type_flag: bool = False) -> Union[DType, Tuple[DType, bool]]:
  """Convenience function to apply JAX argument dtype promotion.

  Args:
    return_weak_type_flag : if True, then return a ``(dtype, weak_type)`` tuple.
      If False, just return `dtype`

  Returns:
    dtype or (dtype, weak_type) depending on the value of the ``return_weak_type`` argument.
  """
  if len(args) == 0:
    raise ValueError("at least one array or dtype is required")
  dtype, weak_type = _lattice_result_type(*(float_ if arg is None else arg for arg in args))
  if weak_type:
    if _fp8_enabled:
      dtype = canonicalize_dtype(
        _default_types['f' if dtype in [_float8_e4m3fn_dtype, _float8_e5m2_dtype, _bfloat16_dtype] else dtype.kind])
    else:
      dtype = canonicalize_dtype(
        _default_types['f' if dtype == _bfloat16_dtype else dtype.kind])
  else:
    dtype = canonicalize_dtype(dtype)
  return (dtype, weak_type) if return_weak_type_flag else dtype
