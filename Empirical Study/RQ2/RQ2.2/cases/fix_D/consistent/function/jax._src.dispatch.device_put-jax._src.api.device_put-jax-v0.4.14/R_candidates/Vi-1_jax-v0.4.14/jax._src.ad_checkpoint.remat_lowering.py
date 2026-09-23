def remat_lowering(*args, jaxpr: core.Jaxpr, prevent_cse: bool,
                   differentiated: bool, is_gpu_platform: bool = False,
                   **_):
  assert not jaxpr.constvars

  if differentiated and prevent_cse:
    if config.jax_remat_opt_barrier:
      translation_rule = _remat_translation_using_opt_barrier
    elif is_gpu_platform:
      translation_rule = _remat_translation_using_while
    else:
      translation_rule = _remat_translation_using_cond
  else:
    translation_rule = lambda *args, jaxpr: core.eval_jaxpr(jaxpr, (), *args)

  return api.named_call(translation_rule, name="remat")(*args, jaxpr=jaxpr)
