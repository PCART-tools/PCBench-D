def primal_dtype_to_tangent_dtype(primal_dtype):
  # TODO(frostig,mattjj): determines that all opaque dtypes have
  # float0 tangent type, which works fine for all our current opaque
  # dtype applications. We may some day want to delegate this
  # decision to the dtype rules.
  if (is_opaque_dtype(primal_dtype) or
      not dtypes.issubdtype(primal_dtype, np.inexact)):
    return dtypes.float0
  else:
    return primal_dtype
