@weakref_lru_cache
def _fori_body_fun(body_fun):
  body_fun = weakref.ref(body_fun)
  def while_body_fun(loop_carry):
    i, upper, x = loop_carry
    return lax.add(i, lax._const(i, 1)), upper, body_fun()(i, x)
  return while_body_fun
