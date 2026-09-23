@util.cache()
def xla_primitive_callable(prim, *arg_specs: ArgSpec, **params):
  donated_invars = (False,) * len(arg_specs)
  def prim_fun(*args):
    out = prim.bind(*args, **params)
    if prim.multiple_results:
      return out
    else:
      return out,
  compiled = _xla_callable_uncached(lu.wrap_init(prim_fun), prim.name,
                                    donated_invars, False, *arg_specs)
  if not prim.multiple_results:
    return lambda *args, **kw: compiled(*args, **kw)[0]
  else:
    return compiled
