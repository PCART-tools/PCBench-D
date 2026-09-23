  def __init__(self, shape, dtype, named_shape=None, sharding=None):
    self.shape = tuple(shape)
    if dtype is None:
      raise ValueError("ShapeDtypeStruct: dtype must be specified.")
    self.dtype = dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
    if sharding is not None and not isinstance(sharding, (Sharding, Layout)):
      raise ValueError(
          "sharding should be an instance of `jax.sharding.Sharding` or"
          f" `jax.experimental.layout.Layout`. Got {sharding} of type"
          f" {type(sharding)}.")
    if (isinstance(sharding, Layout) and
        isinstance(sharding.device_local_layout, AutoLayout)):
      raise TypeError(
          "`DeviceLocalLayout.AUTO` cannot be used in place of a device-local"
          f" layout in a `ShapeDtypeStruct`. Got {sharding}")
    self.sharding = sharding.sharding if isinstance(sharding, Layout) else sharding
    self._dll = sharding.device_local_layout if isinstance(sharding, Layout) else None
    self.named_shape = {} if named_shape is None else dict(named_shape)
