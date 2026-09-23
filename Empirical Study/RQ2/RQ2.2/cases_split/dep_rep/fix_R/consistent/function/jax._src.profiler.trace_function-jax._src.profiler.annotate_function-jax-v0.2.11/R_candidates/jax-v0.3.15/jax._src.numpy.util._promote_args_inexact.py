def _promote_args_inexact(fun_name, *args):
  """Convenience function to apply Numpy argument shape and dtype promotion.

  Promotes non-inexact types to an inexact type."""
  _check_arraylike(fun_name, *args)
  _check_no_float0s(fun_name, *args)
  return _promote_shapes(fun_name, *_promote_dtypes_inexact(*args))
