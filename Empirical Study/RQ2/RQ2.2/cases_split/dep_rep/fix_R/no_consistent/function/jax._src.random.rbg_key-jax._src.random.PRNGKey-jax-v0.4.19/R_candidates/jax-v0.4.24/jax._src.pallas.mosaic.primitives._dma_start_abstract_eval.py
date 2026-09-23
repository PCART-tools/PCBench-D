@dma_start_p.def_abstract_eval
def _dma_start_abstract_eval(*args, tree, device_id_type):
  (
      src_ref_aval,
      src_indexers_avals,
      dst_ref_aval,
      dst_indexers_avals,
      dst_sem_aval,
      dst_sem_indexers_avals,
      src_sem_aval,
      src_sem_indexers_avals,
      device_id_aval,
  ) = tree_util.tree_unflatten(tree, args)
  dst_sem_shape = dst_sem_aval.shape
  if dst_sem_indexers_avals:
    dst_sem_shape = dst_sem_indexers_avals[-1].get_indexer_shape()
  if dst_sem_shape:
    raise ValueError(
        f"Cannot signal on a non-()-shaped semaphore: {dst_sem_shape}"
    )
  if src_sem_aval is not None:
    src_sem_shape = src_sem_aval.shape
    if src_sem_indexers_avals:
      src_sem_shape = src_sem_indexers_avals[-1].get_indexer_shape()
    if src_sem_shape:
      raise ValueError(
          f"Cannot signal on a non-()-shaped semaphore: {src_sem_shape}"
      )
  return []
