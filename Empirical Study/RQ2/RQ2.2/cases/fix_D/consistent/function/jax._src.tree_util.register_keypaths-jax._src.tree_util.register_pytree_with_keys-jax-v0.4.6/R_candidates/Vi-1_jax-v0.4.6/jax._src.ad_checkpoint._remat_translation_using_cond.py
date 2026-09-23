def _remat_translation_using_cond(*args, jaxpr: core.Jaxpr):
  # Implements:
  #  if(rng(0, 1) < 2)
  #    return eval_jaxpr(*args)
  #  else:
  #    return 0
  avals_out = tuple(v.aval for v in jaxpr.outvars)

  def remat_comp(*args):
    return tuple(core.eval_jaxpr(jaxpr, (), *args))
  def dummy_comp(*args):
    return tuple(map(_dummy_like, avals_out))

  unif = jax.lax.rng_uniform(np.float32(0), np.float32(1), shape=())
  return jax.lax.cond(unif < np.float32(2), remat_comp, dummy_comp, *args)
