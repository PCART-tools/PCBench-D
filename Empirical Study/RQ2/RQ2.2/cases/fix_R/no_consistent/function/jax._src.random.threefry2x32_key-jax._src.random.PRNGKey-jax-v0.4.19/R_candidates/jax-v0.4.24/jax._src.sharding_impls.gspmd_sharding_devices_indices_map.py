@functools.lru_cache(maxsize=4096)
def gspmd_sharding_devices_indices_map(
    self, global_shape: Shape) -> Mapping[Device, Index]:
  self.shard_shape(global_shape)  # raises a good error message
  indices = op_sharding_to_indices(self._hlo_sharding, global_shape,
                                    len(self._devices))
  return dict(safe_zip(self._devices, indices))
