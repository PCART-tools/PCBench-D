def instantiate_zeros_aval(aval, tangent):
  if type(tangent) is Zero:
    assert tangent.aval == aval
    return zeros_like_aval(aval)
  else:
    return tangent
