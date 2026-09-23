@functools.lru_cache(maxsize=4096)
def _positional_sharding_to_xla_hlo_sharding(
    self, num_dimensions: int) -> xc.HloSharding:
  if self.shape == (1,) * self.ndim:
    return get_replicated_hlo_sharding()

  pbuf = xc.OpSharding()
  shape = self.shape[self.ndim - num_dimensions:]  # 'rank promotion' of val
  set_size, = {len(device_set) for device_set in self._ids.flat}
  pbuf.type = xc.OpSharding.Type.OTHER
  if set_size > 1:
    pbuf.last_tile_dims = [xc.OpSharding.Type.REPLICATED]
    pbuf.tile_assignment_dimensions = (*shape, set_size)
  else:
    pbuf.tile_assignment_dimensions = shape
  pbuf.tile_assignment_devices = [i for ids in self._ids.flat for i in ids]
  product_of_dims = math.prod(pbuf.tile_assignment_dimensions)
  num_devices = len(pbuf.tile_assignment_devices)
  assert product_of_dims == num_devices, (product_of_dims, num_devices)
  return xc.HloSharding.from_proto(pbuf)
