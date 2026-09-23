@lru_cache()
def create_mesh_pspec_sharding(
    mesh: Mesh, pspec: PartitionSpec, parsed_pspec=None
) -> sharding_impls.NamedSharding:
  return sharding_impls.NamedSharding(mesh, pspec, parsed_pspec)
