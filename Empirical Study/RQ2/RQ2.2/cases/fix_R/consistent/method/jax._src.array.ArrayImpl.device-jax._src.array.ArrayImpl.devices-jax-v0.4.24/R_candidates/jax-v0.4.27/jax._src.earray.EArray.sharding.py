  @property
  def sharding(self):
    phys_sharding = self._data.sharding
    return self.aval.dtype._rules.logical_sharding(self.aval, phys_sharding)
