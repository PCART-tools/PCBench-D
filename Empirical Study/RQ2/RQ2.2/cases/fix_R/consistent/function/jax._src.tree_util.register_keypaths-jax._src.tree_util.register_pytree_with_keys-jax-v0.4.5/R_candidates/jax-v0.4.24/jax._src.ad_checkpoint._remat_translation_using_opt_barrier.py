def _remat_translation_using_opt_barrier(*args, jaxpr: core.Jaxpr):
  args = _optimization_barrier(args)
  return core.eval_jaxpr(jaxpr, (), *args)
