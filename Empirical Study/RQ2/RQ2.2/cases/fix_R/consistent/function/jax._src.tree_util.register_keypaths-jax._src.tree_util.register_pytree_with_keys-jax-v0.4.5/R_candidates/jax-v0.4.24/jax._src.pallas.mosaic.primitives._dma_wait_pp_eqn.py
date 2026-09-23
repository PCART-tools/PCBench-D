def _dma_wait_pp_eqn(eqn: jax_core.JaxprEqn,
                     context: jax_core.JaxprPpContext,
                     settings: jax_core.JaxprPpSettings):
  del settings
  invars = eqn.invars
  tree = eqn.params["tree"]
  sem, sem_indexers, ref, indexers = tree_util.tree_unflatten(tree, invars)
  return pp.concat([
      pp.text('dma_wait'),
      pp.text(' '),
      sp.pp_ref_indexers(context, ref, indexers),
      pp.text(' '),
      sp.pp_ref_indexers(context, sem, sem_indexers),
  ])
