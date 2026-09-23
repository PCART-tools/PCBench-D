def _dma_wait_lowering_rule(ctx: LoweringRuleContext, *args, tree,
                            device_id_type: tpu_primitives.DeviceIdType):
  del device_id_type
  sem, sem_indexers, ref, indexers = tree_util.tree_unflatten(tree, args)
  sem_aval, _, ref_aval, _ = tree_util.tree_unflatten(tree, ctx.avals_in)
  block_shapes = tree_util.tree_unflatten(tree, ctx.block_shapes)
  ref_block_shape = block_shapes[2]
  ref, _, _ = _index_ref(
      ref, ref_aval, ref_block_shape, indexers
  )
  sem, _, _ = _index_ref(sem, sem_aval, sem_aval.shape, sem_indexers)
  return tpu.WaitDMAOp(sem, ref).results
