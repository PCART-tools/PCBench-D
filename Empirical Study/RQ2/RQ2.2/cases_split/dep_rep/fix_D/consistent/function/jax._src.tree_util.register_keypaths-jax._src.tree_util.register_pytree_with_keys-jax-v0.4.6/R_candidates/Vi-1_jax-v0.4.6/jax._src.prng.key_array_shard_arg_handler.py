def key_array_shard_arg_handler(x: PRNGKeyArray, devices, indices, sharding):
  # TODO(frostig): Remove the need for `core.get_aval`.
  aval = core.get_aval(x)
  key_shape = aval.dtype.impl.key_shape
  arr = x.unsafe_raw_array()

  # TODO(yashkatariya,frostig): This assumes that the last dimensions are not
  # sharded. This is only true when enable_custom_prng is True.
  trailing_inds = [slice(None)] * len(key_shape)
  phys_indices = [(*inds, *trailing_inds) for inds in indices]
  phys_sharding = make_key_array_phys_sharding(
      aval, sharding, is_sharding_from_xla=False)
  return pxla.shard_arg_handlers[type(arr)](
      arr, devices, phys_indices, phys_sharding
  )
