  def __str__(self):
    device_ids = [d.id for d in self.devices.flat]
    return (f'PmapSharding(sharding_spec={self.sharding_spec}, '
            f'{device_ids=}, '
            f'device_platform={self.devices.flat[0].platform.upper()}, '
            f'device_shape={self.devices.shape})')
