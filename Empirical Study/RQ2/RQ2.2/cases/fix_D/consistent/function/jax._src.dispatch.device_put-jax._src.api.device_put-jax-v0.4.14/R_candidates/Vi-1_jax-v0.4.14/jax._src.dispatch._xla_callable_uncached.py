def _xla_callable_uncached(fun: lu.WrappedFun, name, donated_invars,
                           keep_unused, in_avals, orig_in_shardings):
  computation = sharded_lowering(
      fun, name, donated_invars, keep_unused, True, in_avals, orig_in_shardings,
      lowering_platform=None)
  return computation.compile().unsafe_call
