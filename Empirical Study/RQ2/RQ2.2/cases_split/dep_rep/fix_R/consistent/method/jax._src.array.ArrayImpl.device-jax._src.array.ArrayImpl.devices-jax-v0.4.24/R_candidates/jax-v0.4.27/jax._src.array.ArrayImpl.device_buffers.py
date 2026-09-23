  @property
  def device_buffers(self):
    raise AttributeError(
      "arr.device_buffers has been deprecated. Use [x.data for x in arr.addressable_shards]")
