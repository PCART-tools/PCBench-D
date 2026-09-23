  @staticmethod
  def check_replicated_trailing_dims(sharding: XLACompatibleSharding, aval):
    if isinstance(sharding, PmapSharding):
      return
    phys_aval = core.physical_aval(aval)
    hlo_s = sharding._to_xla_hlo_sharding(phys_aval.ndim)
    partitions, _ = op_shardings.get_num_ways_dim_sharded(hlo_s)
    num_trailing_dims = phys_aval.ndim - aval.ndim
    if not all(i == 1 for i in partitions[-num_trailing_dims:]):
      raise AssertionError(
          "The trailing dims of extended dtypes should be replicated. Got"
          f" sharding: {sharding}, partitions: {partitions}, "
          f"num_trailing_dims: {num_trailing_dims}")
