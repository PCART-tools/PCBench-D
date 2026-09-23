def _sda_copy_to_host_async(self):
  for buffer_index in self.one_replica_buffer_indices:
    self.device_buffers[buffer_index].copy_to_host_async()
