def instantiate_zeros(tangent):
  return zeros_like_aval(tangent.aval) if type(tangent) is Zero else tangent
