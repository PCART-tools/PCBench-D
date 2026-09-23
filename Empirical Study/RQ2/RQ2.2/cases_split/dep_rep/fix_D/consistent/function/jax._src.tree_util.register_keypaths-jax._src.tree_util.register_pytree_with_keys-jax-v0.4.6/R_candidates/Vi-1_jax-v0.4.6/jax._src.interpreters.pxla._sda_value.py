def _sda_value(self):
  if self._npy_value is None:
    self.copy_to_host_async()
    npy_value = np.empty(self.aval.shape, self.aval.dtype)
    for i in self.one_replica_buffer_indices:
      npy_value[self.indices[i]] = np.asarray(self.device_buffers[i])
    self._npy_value = npy_value
  return self._npy_value
