def promote_args(fun_name: str, *args: ArrayLike) -> list[Array]:
  """Convenience function to apply Numpy argument shape and dtype promotion."""
  check_arraylike(fun_name, *args)
  _check_no_float0s(fun_name, *args)
  check_for_prngkeys(fun_name, *args)
  return promote_shapes(fun_name, *promote_dtypes(*args))
