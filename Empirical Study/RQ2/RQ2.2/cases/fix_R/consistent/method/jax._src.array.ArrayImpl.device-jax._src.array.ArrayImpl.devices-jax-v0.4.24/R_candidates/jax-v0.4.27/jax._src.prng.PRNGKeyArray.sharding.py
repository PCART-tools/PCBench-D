  @property
  def sharding(self):
    phys_sharding = self._base_array.sharding
    return KeyTyRules.logical_sharding(self.aval, phys_sharding)
