def _promote_args(fun_name: str, *args: ArrayLike) -> List[Array]:
  """Convenience function to apply Numpy argument shape and dtype promotion."""
  _check_arraylike(fun_name, *args)
  _check_no_float0s(fun_name, *args)
  return _promote_shapes(fun_name, *_promote_dtypes(*args))
