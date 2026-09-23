def primal_dtype_to_tangent_dtype(primal_dtype):
  if dtypes.issubdtype(primal_dtype, dtypes.extended):
    return primal_dtype._rules.tangent_dtype(primal_dtype)  # type: ignore
  elif not dtypes.issubdtype(primal_dtype, np.inexact):
    return dtypes.float0
  else:
    return primal_dtype
