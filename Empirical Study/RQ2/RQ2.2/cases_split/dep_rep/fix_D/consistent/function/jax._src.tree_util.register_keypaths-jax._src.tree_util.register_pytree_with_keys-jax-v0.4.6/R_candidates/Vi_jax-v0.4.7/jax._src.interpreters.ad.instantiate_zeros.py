def instantiate_zeros(tangent):
  if type(tangent) is Zero:
    return zeros_like_aval(tangent.aval)
  else:
    return tangent
