@util.cache()
def xla_primitive_callable(prim, in_avals, orig_in_shardings, **params):
  def prim_fun(*args):
    out = prim.bind(*args, **params)
    if prim.multiple_results:
      return out
    else:
      return out,
  donated_invars = (False,) * len(in_avals)
  compiled = _xla_callable_uncached(
      lu.wrap_init(prim_fun), prim.name, donated_invars, False, in_avals,
      orig_in_shardings)
  if not prim.multiple_results:
    return lambda *args, **kw: compiled(*args, **kw)[0]
  else:
    return compiled
