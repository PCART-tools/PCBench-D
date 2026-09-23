def get_array_mapping(pspec: PartitionSpec) -> ArrayMappingOrAutoOrUnspecified:
  parsed_pspec, _, _ = sharding_impls.prepare_axis_resources(
      pspec, "pspec to array_mapping")
  return _get_array_mapping(parsed_pspec)
