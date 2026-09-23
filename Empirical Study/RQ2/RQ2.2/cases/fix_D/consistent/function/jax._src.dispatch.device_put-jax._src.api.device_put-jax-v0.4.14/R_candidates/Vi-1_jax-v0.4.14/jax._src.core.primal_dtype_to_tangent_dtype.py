def primal_dtype_to_tangent_dtype(primal_dtype):
  # TODO(frostig,mattjj): determines that all extended dtypes have
  # float0 tangent type, which works fine for all our current
  # extended dtype applications. We may some day want to delegate
  # this decision to the dtype rules.
  if (dtypes.issubdtype(primal_dtype, dtypes.extended) or
      not dtypes.issubdtype(primal_dtype, np.inexact)):
    return dtypes.float0
  else:
    return primal_dtype
