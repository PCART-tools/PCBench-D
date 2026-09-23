def _semaphore_wait_pp_eqn(eqn: jax_core.JaxprEqn,
                             context: jax_core.JaxprPpContext,
                             settings: jax_core.JaxprPpSettings):
  del settings
  invars = eqn.invars
  tree = eqn.params["args_tree"]
  (
      sem,
      sem_indexers,
      value,
  ) = tree_util.tree_unflatten(tree, invars)
  return pp.concat([
      pp.text('semaphore_wait'),
      pp.text(' '),
      sp.pp_ref_indexers(context, sem, sem_indexers),
      pp.text(' '),
      pp.text(jax_core.pp_var(value, context)),
  ])
