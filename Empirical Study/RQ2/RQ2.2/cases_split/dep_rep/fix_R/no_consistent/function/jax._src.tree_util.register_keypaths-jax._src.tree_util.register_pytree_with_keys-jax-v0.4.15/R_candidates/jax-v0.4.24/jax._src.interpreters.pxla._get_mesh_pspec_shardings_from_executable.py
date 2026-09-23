def _get_mesh_pspec_shardings_from_executable(
    xla_executable, mesh: Mesh
) -> tuple[Sequence[sharding_impls.NamedSharding],
           Sequence[sharding_impls.NamedSharding]]:
  from jax._src import pjit

  in_pspec, out_pspec = pjit.get_pspec_from_executable(xla_executable, mesh)
  return ([sharding_impls.NamedSharding(mesh, i) for i in in_pspec],
          [sharding_impls.NamedSharding(mesh, o) for o in out_pspec])
