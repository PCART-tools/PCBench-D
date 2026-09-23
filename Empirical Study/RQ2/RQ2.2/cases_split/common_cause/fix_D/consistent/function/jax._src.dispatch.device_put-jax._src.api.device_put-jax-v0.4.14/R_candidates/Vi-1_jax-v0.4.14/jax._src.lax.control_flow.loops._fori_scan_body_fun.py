@weakref_lru_cache
def _fori_scan_body_fun(body_fun):
  body_fun = weakref.ref(body_fun)
  def scanned_fun(loop_carry, _):
    i, x = loop_carry
    return (i + 1, body_fun()(i, x)), None
  return scanned_fun
