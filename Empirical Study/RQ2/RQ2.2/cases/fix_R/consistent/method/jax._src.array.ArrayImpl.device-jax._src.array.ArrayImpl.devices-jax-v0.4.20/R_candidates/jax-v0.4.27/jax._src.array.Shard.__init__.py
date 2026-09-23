  def __init__(self, device: Device, sharding: Sharding, global_shape: Shape,
               data: None | ArrayImpl | PRNGKeyArray = None):
    self._device = device
    self._sharding = sharding
    self._global_shape = global_shape
    self._data = data
