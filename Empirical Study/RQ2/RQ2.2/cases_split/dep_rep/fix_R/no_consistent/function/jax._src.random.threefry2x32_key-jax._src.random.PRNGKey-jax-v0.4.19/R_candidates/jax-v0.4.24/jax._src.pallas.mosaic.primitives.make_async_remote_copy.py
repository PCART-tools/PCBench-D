def make_async_remote_copy(src_ref, dst_ref, send_sem, recv_sem, device_id,
                           device_id_type: DeviceIdType = DeviceIdType.MESH):
  src_ref, src_indexers = _get_ref_and_indexers(src_ref)
  send_sem, send_sem_indexers = _get_ref_and_indexers(send_sem)
  dst_ref, dst_indexers = _get_ref_and_indexers(dst_ref)
  recv_sem, recv_sem_indexers = _get_ref_and_indexers(recv_sem)
  return AsyncCopyDescriptor(
      src_ref, src_indexers, dst_ref, dst_indexers, recv_sem, recv_sem_indexers,
      send_sem, send_sem_indexers, device_id, device_id_type=device_id_type)
