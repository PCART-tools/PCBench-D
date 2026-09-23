def _sda_block_until_ready(self):
  self._check_if_deleted()
  for buf in self.device_buffers:
    buf.block_until_ready()
  return self
