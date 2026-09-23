def _sda__getitem__(self, idx):
  self._check_if_deleted()
  if not isinstance(idx, tuple):
    cidx = (idx,) + (slice(None),) * (len(self.aval.shape) - 1)
  else:
    cidx = idx + (slice(None),) * (len(self.aval.shape) - len(idx))
  if self._npy_value is None:
    try:
      buf_idx = self.indices.index(cidx)
    except ValueError:
      buf_idx = None
    if buf_idx is not None:
      buf = self.device_buffers[buf_idx]
      aval = ShapedArray(buf.shape, self.aval.dtype)
      return device_array.make_device_array(aval, None, buf)
  return super(self.__class__, self).__getitem__(idx)
