def zeros_like_aval(aval):
  return aval_zeros_likers[type(aval)](aval)
