def remat_impl(*args,
               call_jaxpr: Optional[core.Jaxpr] = None,
               jaxpr: Optional[core.Jaxpr] = None,
               prevent_cse: bool, differentiated: bool,
               policy,
               is_gpu_platform: bool = False,
               concrete: bool = False,
               name: str = "checkpoint"):
  # Support either "jaxpr" (for remat2) and "call_jaxpr" (for remat)
  # name is not passed for remat2, defaults to "checkpoint"
  # TODO: remove call_jaxpr once we drop the remat call primitive
  if jaxpr is None:
    jaxpr = call_jaxpr
  assert jaxpr is not None
  assert not jaxpr.constvars

  del concrete, policy  # Unused.
  if differentiated and prevent_cse:
    if config.jax_remat_opt_barrier:
      translation_rule = _remat_translation_using_opt_barrier
    elif is_gpu_platform:
      translation_rule = _remat_translation_using_while
    else:
      translation_rule = _remat_translation_using_cond
  else:
    translation_rule = lambda *args, jaxpr: core.eval_jaxpr(jaxpr, (), *args)

  return jax.named_call(translation_rule, name=wrap_name(name, "remat"))(*args, jaxpr=jaxpr)
