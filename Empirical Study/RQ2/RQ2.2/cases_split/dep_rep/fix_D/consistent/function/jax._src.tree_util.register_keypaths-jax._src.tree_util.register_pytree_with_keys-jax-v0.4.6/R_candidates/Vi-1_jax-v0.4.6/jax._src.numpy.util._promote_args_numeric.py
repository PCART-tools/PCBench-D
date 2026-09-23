def _promote_args_numeric(fun_name: str, *args: ArrayLike) -> List[Array]:
  _check_arraylike(fun_name, *args)
  _check_no_float0s(fun_name, *args)
  return _promote_shapes(fun_name, *_promote_dtypes_numeric(*args))
