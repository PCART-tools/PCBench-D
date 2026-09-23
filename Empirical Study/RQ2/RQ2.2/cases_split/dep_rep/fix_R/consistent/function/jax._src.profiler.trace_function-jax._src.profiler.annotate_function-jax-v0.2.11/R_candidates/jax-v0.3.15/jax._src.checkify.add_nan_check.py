def add_nan_check(prim):
  error_checks[prim] = partial(nan_error_check, prim)
