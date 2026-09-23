def _get_mesh_pspec_shardings_from_executable(
    xla_executable, mesh: Mesh
) -> Tuple[Sequence[sharding_internal.NamedSharding],
           Sequence[sharding_internal.NamedSharding]]:
  from jax.experimental import pjit

  in_pspec, out_pspec = pjit._get_pspec_from_executable(xla_executable, mesh)
  return ([sharding_internal.NamedSharding(mesh, i) for i in in_pspec],
          [sharding_internal.NamedSharding(mesh, o) for o in out_pspec])
