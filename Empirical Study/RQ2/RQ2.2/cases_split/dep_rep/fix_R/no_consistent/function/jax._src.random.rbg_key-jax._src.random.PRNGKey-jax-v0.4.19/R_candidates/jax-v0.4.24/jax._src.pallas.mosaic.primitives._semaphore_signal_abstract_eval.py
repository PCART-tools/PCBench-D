@semaphore_signal_p.def_abstract_eval
def _semaphore_signal_abstract_eval(
    *avals,
    args_tree,
    device_id_type: DeviceIdType,
):
  del device_id_type
  sem_aval, sem_indexers_avals, value_aval, device_id_avals = (
      tree_util.tree_unflatten(args_tree, avals)
  )
  if not isinstance(sem_aval, state.AbstractRef):
    raise ValueError(f"Cannot signal on a non-Ref: {sem_aval}")
  sem_shape = sem_aval.shape
  if sem_indexers_avals:
    sem_shape = sem_indexers_avals[-1].get_indexer_shape()
  if sem_shape:
    raise ValueError(f"Cannot signal on a non-()-shaped semaphore: {sem_shape}")
  sem_dtype = sem_aval.dtype
  if not (jnp.issubdtype(sem_dtype, tpu_core.semaphore) or jnp.issubdtype(
      sem_dtype, tpu_core.barrier_semaphore)):
    raise ValueError(f"Must signal a REGULAR or BARRIER semaphore: {sem_dtype}")
  if value_aval.dtype != jnp.dtype("int32"):
    raise ValueError("Must signal an int32 value.")
  if device_id_avals is not None:
    device_id_flat_avals = tree_util.tree_leaves(device_id_avals)
    for aval in device_id_flat_avals:
      if aval.dtype != jnp.dtype("int32"):
        raise ValueError("`device_id`s must be an int32 value.")
  return []
