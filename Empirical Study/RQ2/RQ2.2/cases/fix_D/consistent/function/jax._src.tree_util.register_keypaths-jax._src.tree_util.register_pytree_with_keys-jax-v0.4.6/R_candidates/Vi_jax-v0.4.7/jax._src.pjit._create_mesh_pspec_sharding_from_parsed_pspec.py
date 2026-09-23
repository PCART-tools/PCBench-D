@lru_cache(maxsize=4096)
def _create_mesh_pspec_sharding_from_parsed_pspec(mesh, x):
  if _is_unspecified_or_from_gda_or_auto(x):
    return x
  return pxla.create_mesh_pspec_sharding(mesh, x.user_spec, x)
