  def is_compatible_aval(self, aval_shape: Shape):
    num_ways_dim_sharded, _ = get_num_ways_dim_sharded(self._hlo_sharding)
    if len(aval_shape) < len(num_ways_dim_sharded):
      raise ValueError(
          f"Sharding {self} is only valid for values of rank at least "
          f"{len(num_ways_dim_sharded)}, but was applied to a value of rank "
          f"{len(aval_shape)}")
