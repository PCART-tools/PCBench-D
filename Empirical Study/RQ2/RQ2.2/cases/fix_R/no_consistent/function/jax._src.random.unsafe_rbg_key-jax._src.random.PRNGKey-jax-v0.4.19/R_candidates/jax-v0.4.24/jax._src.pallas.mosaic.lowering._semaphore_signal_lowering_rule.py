def _semaphore_signal_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    args_tree,
    device_id_type: tpu_primitives.DeviceIdType,
):
  sem_aval, _, _, _ = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  sem, indexers, value, device_id = tree_util.tree_unflatten(args_tree, args)
  sem, _, _ = _index_ref(sem, sem_aval, sem_aval.shape, indexers)
  if device_id is not None:
    device_id = _device_id_to_logical(ctx, device_id, device_id_type)
  return tpu.SemaphoreSignalOp(sem, value, device_id=device_id).results
