def _sda_check_if_deleted(self):
  if self.device_buffers is None:
    raise ValueError("ShardedDeviceArray has been deleted.")
