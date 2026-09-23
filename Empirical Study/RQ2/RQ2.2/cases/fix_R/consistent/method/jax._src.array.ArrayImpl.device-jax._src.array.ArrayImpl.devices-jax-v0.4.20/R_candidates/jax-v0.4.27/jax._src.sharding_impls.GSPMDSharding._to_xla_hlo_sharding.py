  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    return self._hlo_sharding
