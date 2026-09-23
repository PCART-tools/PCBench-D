def _get_pmap_sharding(devices, specs):
  return [sharding_internal.PmapSharding(devices, spec) for spec in specs]
