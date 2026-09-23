  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    return _positional_sharding_to_xla_hlo_sharding(self, num_dimensions)
