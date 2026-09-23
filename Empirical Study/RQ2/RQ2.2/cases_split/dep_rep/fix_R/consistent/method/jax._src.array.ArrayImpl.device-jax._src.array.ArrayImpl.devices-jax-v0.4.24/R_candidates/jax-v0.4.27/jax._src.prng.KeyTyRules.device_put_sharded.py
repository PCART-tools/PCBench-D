  @staticmethod
  def device_put_sharded(vals, aval, sharding, devices):
    physical_aval = core.physical_aval(aval)
    physical_buffers = tree_util.tree_map(random_unwrap, vals)
    physical_sharding = make_key_array_phys_sharding(aval, sharding)
    physical_result = pxla.batched_device_put(physical_aval, physical_sharding, physical_buffers, list(devices))
    return random_wrap(physical_result, impl=aval.dtype._impl)
