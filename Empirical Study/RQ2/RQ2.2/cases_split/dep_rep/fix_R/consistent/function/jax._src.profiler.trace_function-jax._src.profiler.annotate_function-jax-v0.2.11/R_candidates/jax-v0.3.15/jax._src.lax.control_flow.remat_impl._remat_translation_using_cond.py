def _remat_translation_using_cond(*args,
                                  jaxpr: core.Jaxpr):
  # Implements:
  #  if(rng(0, 1) < 2)
  #    return eval_jaxpr(*args)
  #  else:
  #    return 0
  avals_out = tuple(ov.aval for ov in jaxpr.outvars)

  def remat_comp(*args):
    return tuple(core.eval_jaxpr(jaxpr, (), *args))
  def dummy_comp(*args):
    return tuple(_map(_dummy_remat_result, avals_out))

  cond_pred = (lax.rng_uniform(np.float32(0), np.float32(1), shape=()) < np.float32(2))
  return cond(cond_pred, remat_comp, dummy_comp, *args)
