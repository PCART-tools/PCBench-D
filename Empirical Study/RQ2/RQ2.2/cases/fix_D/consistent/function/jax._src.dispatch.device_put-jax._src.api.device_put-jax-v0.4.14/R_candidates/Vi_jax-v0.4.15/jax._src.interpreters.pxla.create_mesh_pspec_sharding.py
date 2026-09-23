@lru_cache
def create_mesh_pspec_sharding(
    mesh: Mesh, pspec: Optional[PartitionSpec], parsed_pspec=None,
    memory_kind: Optional[str] = None) -> sharding_impls.NamedSharding:
  if pspec is None:
    pspec, parsed_pspec = PartitionSpec(), None
  return sharding_impls.NamedSharding(mesh, pspec, _parsed_pspec=parsed_pspec,
                                      memory_kind=memory_kind)
