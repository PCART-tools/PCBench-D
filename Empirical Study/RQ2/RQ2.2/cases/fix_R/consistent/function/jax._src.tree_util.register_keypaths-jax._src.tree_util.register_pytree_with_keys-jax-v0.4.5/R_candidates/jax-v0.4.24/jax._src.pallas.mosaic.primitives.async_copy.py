def async_copy(src_ref, dst_ref, sem):
  """Issues a DMA copying from src_ref to dst_ref."""
  copy_descriptor = make_async_copy(src_ref, dst_ref, sem)
  copy_descriptor.start()
  return copy_descriptor
