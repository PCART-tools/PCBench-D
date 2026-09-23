  @staticmethod
  def logical_sharding(aval, phys_sharding) -> XLACompatibleSharding:
    # The trailing dims should always be replicated.
    aval.dtype._rules.check_replicated_trailing_dims(phys_sharding, aval)

    if dispatch.is_single_device_sharding(phys_sharding):
      return phys_sharding
    elif isinstance(phys_sharding, PmapSharding):
      key_shape = aval.dtype._impl.key_shape
      logical_sharding_spec = sharding_specs.ShardingSpec(
          sharding=phys_sharding.sharding_spec.sharding[:-len(key_shape)],
          mesh_mapping=phys_sharding.sharding_spec.mesh_mapping)
      return PmapSharding(devices=phys_sharding.devices,
                          sharding_spec=logical_sharding_spec)
    elif isinstance(phys_sharding, NamedSharding):
      logical_gs = get_logical_gspmd_sharding(aval, phys_sharding)
      return pxla._gspmd_to_named_sharding_via_mesh(
          logical_gs, phys_sharding.mesh)
    else:
      return get_logical_gspmd_sharding(aval, phys_sharding)
