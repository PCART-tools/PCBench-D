  @profiler.annotate_function
  def copy_to_host_async(self):
    self._check_if_deleted()
    if self._npy_value is None:
      if self.is_fully_replicated:
        self._copy_single_device_array_to_host_async()
        return
      for i, _ in _cached_index_calc(self.sharding, self.shape):
        self._arrays[i]._copy_single_device_array_to_host_async()
