def replace_float0s(primal, tangent):
  if dtype(tangent) == float0:
    return zeros_like_jaxval(primal)
  else:
    return tangent
