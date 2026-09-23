def sda_array_result_handler(aval: ShapedArray, sharding, indices):
  sharding_spec = _get_sharding_specs([sharding], [aval])[0]
  if core.is_opaque_dtype(aval.dtype):
    return aval.dtype._rules.local_sharded_result_handler(
        aval, sharding, indices)
  else:
    return lambda bufs: make_sharded_device_array(aval, sharding_spec, bufs,
                                                  indices)
