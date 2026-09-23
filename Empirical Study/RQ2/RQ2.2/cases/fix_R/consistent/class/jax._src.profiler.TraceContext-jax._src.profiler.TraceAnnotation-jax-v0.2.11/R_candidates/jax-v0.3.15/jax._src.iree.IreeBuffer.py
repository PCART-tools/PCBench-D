class IreeBuffer(xla_client.DeviceArrayBase):

  def __init__(self, client, device, buffer):
    self.client = client
    self._device = device
    assert device is not None
    self._buffer = buffer

  def copy_to_device(self, device):
    return self

  def to_py(self) -> np.ndarray:
    return np.asarray(self._buffer)

  def to_iree(self):
    return self._buffer

  def platform(self):
    return self.client.platform

  def device(self):
    return self._device

  def block_until_ready(self) -> IreeBuffer:
    return self  # no async

  # overrides repr on base class which expects _value and aval attributes
  def __repr__(self): return f'IreeBuffer({self.to_py()})'
  _value = property(to_py)
