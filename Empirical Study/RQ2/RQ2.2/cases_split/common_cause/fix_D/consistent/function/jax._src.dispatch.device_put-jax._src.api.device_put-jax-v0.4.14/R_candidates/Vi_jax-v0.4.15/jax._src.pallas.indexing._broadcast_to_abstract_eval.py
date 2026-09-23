@broadcast_to_p.def_abstract_eval
def _broadcast_to_abstract_eval(aval, *, shape):
  return jax_core.ShapedArray(shape, aval.dtype)
