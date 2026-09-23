@lru_cache()
def create_mesh_pspec_sharding(
    mesh: Mesh, pspec: PartitionSpec, parsed_pspec=None
) -> sharding_internal.NamedSharding:
  return sharding_internal.NamedSharding(mesh, pspec, parsed_pspec)
