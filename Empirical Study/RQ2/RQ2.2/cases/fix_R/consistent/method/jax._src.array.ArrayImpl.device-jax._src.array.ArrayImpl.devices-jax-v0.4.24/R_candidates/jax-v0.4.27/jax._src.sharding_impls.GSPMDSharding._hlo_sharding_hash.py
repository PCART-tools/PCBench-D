  @functools.cached_property
  def _hlo_sharding_hash(self):
    if self.is_fully_replicated:
      return hash(get_replicated_hlo_sharding())
    return hash(self._hlo_sharding)
