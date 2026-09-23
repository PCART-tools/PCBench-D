  @use_cpp_method()
  def _copy_single_device_array_to_host_async(self):
    self._arrays[0].copy_to_host_async()
