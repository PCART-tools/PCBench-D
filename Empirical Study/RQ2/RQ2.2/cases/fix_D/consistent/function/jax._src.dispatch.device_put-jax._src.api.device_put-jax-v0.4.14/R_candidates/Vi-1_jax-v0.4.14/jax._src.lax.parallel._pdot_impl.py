@pdot_p.def_impl
def _pdot_impl(x, y, *, axis_name, pos_contract, pos_batch, precision):
  if axis_name: raise NameError(f"unbound axis name: {axis_name[0]}")
  return lax.dot_general(x, y, (pos_contract, pos_batch), precision=precision)
