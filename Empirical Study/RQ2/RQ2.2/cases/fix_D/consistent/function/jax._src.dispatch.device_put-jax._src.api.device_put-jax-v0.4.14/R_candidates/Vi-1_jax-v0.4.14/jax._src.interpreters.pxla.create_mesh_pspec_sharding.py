@lru_cache
def create_mesh_pspec_sharding(
    mesh: Mesh, pspec: PartitionSpec | None, parsed_pspec=None
) -> sharding_impls.NamedSharding:
  if pspec is None:
    pspec, parsed_pspec = PartitionSpec(), None
  return sharding_impls.NamedSharding(mesh, pspec, _parsed_pspec=parsed_pspec)
