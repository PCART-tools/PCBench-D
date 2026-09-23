def zeros_like_aval(aval: core.AbstractValue) -> Array:
  return aval_zeros_likers[type(aval)](aval)
