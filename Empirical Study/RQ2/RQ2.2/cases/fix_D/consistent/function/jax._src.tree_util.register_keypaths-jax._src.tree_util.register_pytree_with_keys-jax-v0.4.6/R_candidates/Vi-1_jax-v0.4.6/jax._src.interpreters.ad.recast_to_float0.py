def recast_to_float0(primal, tangent):
  if core.primal_dtype_to_tangent_dtype(dtype(primal)) == float0:
    return Zero(get_aval(primal).at_least_vspace())
  else:
    return tangent
