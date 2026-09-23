  def devices_indices_map(self, global_shape: Shape) -> Mapping[Device, Index]:
    return gspmd_sharding_devices_indices_map(self, global_shape)
