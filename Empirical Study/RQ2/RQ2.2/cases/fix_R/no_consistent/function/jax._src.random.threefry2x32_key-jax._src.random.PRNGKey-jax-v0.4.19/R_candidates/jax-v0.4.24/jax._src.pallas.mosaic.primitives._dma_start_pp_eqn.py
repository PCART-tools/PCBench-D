def _dma_start_pp_eqn(eqn: jax_core.JaxprEqn,
                      context: jax_core.JaxprPpContext,
                      settings: jax_core.JaxprPpSettings):
  invars = eqn.invars
  tree = eqn.params["tree"]
  (
      src_ref,
      src_indexers,
      dst_ref,
      dst_indexers,
      dst_sem,
      dst_sem_indexers,
      src_sem,
      src_sem_indexers,
      device_id,
  ) = tree_util.tree_unflatten(tree, invars)
  del src_sem_indexers
  # TODO(sharadmv): pretty print source semaphores and device id
  if src_sem or device_id:
    return jax_core._pp_eqn(eqn, context, settings)
  return pp.concat([
      pp.text('dma_start'),
      pp.text(' '),
      sp.pp_ref_indexers(context, src_ref, src_indexers),
      pp.text(' -> '),
      sp.pp_ref_indexers(context, dst_ref, dst_indexers),
      pp.text(' '),
      sp.pp_ref_indexers(context, dst_sem, dst_sem_indexers),
  ])
