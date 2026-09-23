def make_async_copy(src_ref, dst_ref, sem):
  """Issues a DMA copying from src_ref to dst_ref."""
  src_ref, src_indexers = _get_ref_and_indexers(src_ref)
  dst_ref, dst_indexers = _get_ref_and_indexers(dst_ref)
  sem, sem_indexers = _get_ref_and_indexers(sem)
  return AsyncCopyDescriptor(src_ref, src_indexers, dst_ref, dst_indexers,
                             sem, sem_indexers, None, None, None,
                             DeviceIdType.MESH)
