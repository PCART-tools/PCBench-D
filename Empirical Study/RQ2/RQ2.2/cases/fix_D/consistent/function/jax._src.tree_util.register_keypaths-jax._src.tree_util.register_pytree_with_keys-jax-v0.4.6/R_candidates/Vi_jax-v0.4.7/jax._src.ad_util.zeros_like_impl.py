@zeros_like_p.def_impl
def zeros_like_impl(example):
  return jaxval_zeros_likers[type(example)](example)
