def get_array_mapping(pspec: PartitionSpec) -> ArrayMappingOrAutoOrUnspecified:
  # Import here to avoid cyclic import error when importing gda in pjit.py.
  from jax.experimental.pjit import get_array_mapping as _get_array_mapping, _prepare_axis_resources

  parsed_pspec, _, _ = _prepare_axis_resources(pspec, "pspec to array_mapping")
  return _get_array_mapping(parsed_pspec)
