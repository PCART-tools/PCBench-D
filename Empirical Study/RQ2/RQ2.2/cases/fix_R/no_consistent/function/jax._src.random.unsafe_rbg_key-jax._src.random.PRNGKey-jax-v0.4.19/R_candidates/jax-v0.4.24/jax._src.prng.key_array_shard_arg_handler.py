def key_array_shard_arg_handler(x: PRNGKeyArray, sharding):
  arr = x._base_array
  phys_sharding = make_key_array_phys_sharding(
      x.aval, sharding, is_sharding_from_xla=False)
  return pxla.shard_arg_handlers[type(arr)](arr, phys_sharding)
