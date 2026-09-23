def _pjit_abstract_eval(*args, jaxpr, out_shardings, resource_env,
                        out_positional_semantics, **_):
  if config.jax_array:
    return jaxpr.out_avals, jaxpr.effects
  return global_to_local(out_positional_semantics, jaxpr.out_avals,
                         out_shardings, resource_env.physical_mesh), jaxpr.effects
