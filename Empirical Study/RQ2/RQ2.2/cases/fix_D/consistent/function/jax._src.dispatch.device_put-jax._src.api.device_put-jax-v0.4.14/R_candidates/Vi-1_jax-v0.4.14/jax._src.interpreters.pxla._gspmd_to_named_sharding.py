def _gspmd_to_named_sharding(
    op_sharding: xc.OpSharding,
    self: sharding_impls.NamedSharding) -> sharding_impls.NamedSharding:
  parsed_pspec = sharding_impls.parse_flatten_op_sharding(
      op_sharding, self.mesh)[0]
  return create_mesh_pspec_sharding(
      self.mesh, parsed_pspec.get_partition_spec(), parsed_pspec)
