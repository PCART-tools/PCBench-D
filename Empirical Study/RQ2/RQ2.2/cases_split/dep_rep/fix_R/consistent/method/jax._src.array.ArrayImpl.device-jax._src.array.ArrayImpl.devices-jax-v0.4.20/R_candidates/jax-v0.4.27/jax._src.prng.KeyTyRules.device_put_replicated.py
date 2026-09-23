  @staticmethod
  def device_put_replicated(val, aval, sharding, devices):
    physical_aval = core.physical_aval(aval)
    assert len(xla.aval_to_xla_shapes(physical_aval)) == 1
    physical_buf = random_unwrap(val)
    physical_sharding = make_key_array_phys_sharding(aval, sharding)
    physical_result = pxla.batched_device_put(physical_aval, physical_sharding, [physical_buf] * len(devices), devices)
    return random_wrap(physical_result, impl=aval.dtype._impl)
