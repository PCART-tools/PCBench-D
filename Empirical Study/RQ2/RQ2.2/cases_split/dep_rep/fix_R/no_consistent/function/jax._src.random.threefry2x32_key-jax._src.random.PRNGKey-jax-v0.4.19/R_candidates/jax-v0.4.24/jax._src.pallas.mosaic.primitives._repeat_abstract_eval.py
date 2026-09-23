@repeat_p.def_abstract_eval
def _repeat_abstract_eval(x, *, repeats, axis):
  shape = list(x.shape)
  shape[axis] *= repeats
  return jax_core.ShapedArray(shape, x.dtype)
