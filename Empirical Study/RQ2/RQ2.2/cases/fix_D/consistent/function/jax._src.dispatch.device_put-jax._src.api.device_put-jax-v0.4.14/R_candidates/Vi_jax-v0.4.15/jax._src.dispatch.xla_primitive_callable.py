@util.cache()
def xla_primitive_callable(
    prim: core.Primitive, in_avals: tuple[core.AbstractValue, ...],
    orig_in_shardings: OrigShardings, **params,
) -> Callable:
  def prim_fun(*args):
    out = prim.bind(*args, **params)
    if prim.multiple_results:
      return out
    else:
      return out,
  donated_invars = (False,) * len(in_avals)
  computation = sharded_lowering(
      lu.wrap_init(prim_fun), prim.name, donated_invars, keep_unused=False,
      inline=True, in_avals=in_avals, in_shardings=orig_in_shardings.shardings,
      lowering_platform=None)
  compiled = computation.compile().unsafe_call
  if not prim.multiple_results:
    return lambda *args, **kw: compiled(*args, **kw)[0]
  else:
    return compiled
