  def _to_xla_hlo_sharding(self, num_dimensions: int) -> xc.HloSharding:
    return get_replicated_hlo_sharding()
