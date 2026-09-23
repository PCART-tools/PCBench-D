def _gspmd_to_named_sharding(
    out_s: sharding_impls.GSPMDSharding,
    orig_in_s: sharding_impls.NamedSharding) -> sharding_impls.NamedSharding:
  parsed_pspec = sharding_impls.parse_flatten_op_sharding(
      out_s._hlo_sharding, orig_in_s.mesh)[0]
  return create_mesh_pspec_sharding(
      orig_in_s.mesh, parsed_pspec.get_partition_spec(), parsed_pspec,
      out_s.memory_kind)
