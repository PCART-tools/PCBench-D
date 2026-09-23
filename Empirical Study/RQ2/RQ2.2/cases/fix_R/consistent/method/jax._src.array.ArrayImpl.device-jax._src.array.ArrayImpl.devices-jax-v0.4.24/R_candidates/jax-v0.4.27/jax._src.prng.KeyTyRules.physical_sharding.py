  @staticmethod
  def physical_sharding(
      aval, sharding: XLACompatibleSharding) -> XLACompatibleSharding:
    return make_key_array_phys_sharding(aval, sharding)
