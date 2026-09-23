@semaphore_wait_p.def_abstract_eval
def _semaphore_wait_abstract_eval(*avals, args_tree):
  sem_aval, sem_indexers_avals, value_aval = tree_util.tree_unflatten(args_tree, avals)
  if not isinstance(sem_aval, state.AbstractRef):
    raise ValueError(f"Cannot signal on a non-semaphore Ref: {sem_aval}")
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
  return []
