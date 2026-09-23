def _dma_start_lowering_rule(ctx: LoweringRuleContext, *args, tree,
                             device_id_type: tpu_primitives.DeviceIdType):
  (
      src_ref,
      src_indexers,
      dst_ref,
      dst_indexers,
      sem,
      sem_indexers,
      src_sem,
      src_sem_indexers,
      device_id,
  ) = tree_util.tree_unflatten(tree, args)
  (src_ref_aval, _, dst_ref_aval, _, sem_aval, _, src_sem_aval, _, _) = (
      tree_util.tree_unflatten(tree, ctx.avals_in)
  )
  block_shapes = tree_util.tree_unflatten(tree, ctx.block_shapes)
  src_ref_block_shape, dst_ref_block_shape = block_shapes[0], block_shapes[2]
  src_ref, _, _ = _index_ref(
      src_ref, src_ref_aval, src_ref_block_shape, src_indexers
  )
  if src_sem is not None:
    src_sem, _, _ = _index_ref(
        src_sem, src_sem_aval, src_sem_aval.shape, src_sem_indexers)
  dst_ref, _, _ = _index_ref(
      dst_ref, dst_ref_aval, dst_ref_block_shape, dst_indexers
  )
  sem, _, _ = _index_ref(sem, sem_aval, sem_aval.shape, sem_indexers)
  if device_id is not None:
    device_id = _device_id_to_logical(ctx, device_id, device_id_type)
  return tpu.EnqueueDMAOp(src_ref, dst_ref, sem, source_semaphore=src_sem,
                          device_id=device_id).results
