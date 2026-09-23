  @use_cpp_method()
  def __init__(self, devices: Sequence[Device] | np.ndarray,
               sharding_spec: sharding_specs.ShardingSpec):
    self.devices = np.asarray(devices)
    # The sharding spec should be pmap's sharding spec.
    self.sharding_spec = sharding_spec
