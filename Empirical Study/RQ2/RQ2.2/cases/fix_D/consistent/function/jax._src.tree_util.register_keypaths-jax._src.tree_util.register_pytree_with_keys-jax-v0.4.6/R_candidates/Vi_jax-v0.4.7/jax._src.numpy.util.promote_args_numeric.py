def promote_args_numeric(fun_name: str, *args: ArrayLike) -> List[Array]:
  check_arraylike(fun_name, *args)
  _check_no_float0s(fun_name, *args)
  return promote_shapes(fun_name, *promote_dtypes_numeric(*args))
