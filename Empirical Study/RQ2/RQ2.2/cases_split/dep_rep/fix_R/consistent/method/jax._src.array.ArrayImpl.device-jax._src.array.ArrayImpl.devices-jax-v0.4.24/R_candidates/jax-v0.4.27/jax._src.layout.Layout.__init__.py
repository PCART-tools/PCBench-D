  def __init__(self, device_local_layout: LayoutOptions = None,
               sharding: ShardingOptions = None):
    # If layout is concrete and sharding is not, error.
    if (isinstance(device_local_layout, DeviceLocalLayout) and
        (sharding is None or is_auto(sharding))):
      raise ValueError(
          'Sharding has to be concrete when layout is of type'
          f' {type(device_local_layout)}. Please pass a'
          ' `jax.sharding.NamedSharding`, `jax.sharding.PositionalSharding` or'
          ' `jax.sharding.SingleDeviceSharding` to the sharding argument. Got'
          f' sharding {sharding}'
      )
    if not isinstance(
        device_local_layout, (DeviceLocalLayout, type(None), AutoLayout)):
      raise TypeError(
          'Invalid value received for the device_local_layout argument.'
          ' Expected values are `None`, `DeviceLocalLayout.AUTO` or an'
          f' instance of `DeviceLocalLayout`. Got {device_local_layout} of'
          f' type {type(device_local_layout)}'
      )
    if not isinstance(
        sharding, (Sharding, type(None), AutoSharding)):
      raise TypeError(
          'Invalid value received for the sharding argument. Expected values'
          ' are `None`, `pjit.AUTO` or an instance of `jax.Sharding`. Got'
          f' {sharding} of type {type(sharding)}')

    self.device_local_layout = device_local_layout
    self.sharding = sharding
