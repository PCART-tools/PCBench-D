def make_key_array_phys_sharding(aval, sharding, is_sharding_from_xla):
  if dispatch.is_single_device_sharding(sharding):
    return sharding
  elif isinstance(sharding, PmapSharding):
    key_shape = aval.dtype.impl.key_shape
    trailing_sharding = [pxla.NoSharding()] * len(key_shape)
    phys_sharding_spec = pxla.ShardingSpec(
        sharding=(*sharding.sharding_spec.sharding, *trailing_sharding),
        mesh_mapping=sharding.sharding_spec.mesh_mapping)
    return PmapSharding(devices=sharding.devices,
                        sharding_spec=phys_sharding_spec)
  elif isinstance(sharding, NamedSharding):
    key_shape = aval.dtype.impl.key_shape
    trailing_spec = [None] * len(key_shape)
    return NamedSharding(
        sharding.mesh,
        pxla.PartitionSpec(*sharding.spec, *trailing_spec))
  elif is_sharding_from_xla:
    return sharding
  else:
    return GSPMDSharding(
        sharding._device_assignment,
        KeyTyRules.physical_op_sharding(aval, sharding))
