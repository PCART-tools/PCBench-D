@weakref_lru_cache
def _pjit_lower_cached(
    jaxpr: core.ClosedJaxpr,
    sdat_in_shardings: SameDeviceAssignmentTuple,
    sdat_out_shardings: SameDeviceAssignmentTuple,
    resource_env,
    donated_invars,
    name: str,
    in_is_global: Sequence[bool],
    keep_unused: bool,
    always_lower: bool,
    *,
    lowering_platform: Optional[str]):
  in_shardings: Tuple[PjitShardingMinusUnspecified, ...] = cast(
      Tuple[PjitShardingMinusUnspecified, ...], sdat_in_shardings.shardings)
  out_shardings: Tuple[PjitSharding, ...] = sdat_out_shardings.shardings

  if resource_env is not None:
    pxla.resource_typecheck(jaxpr, resource_env, {}, lambda: "pjit")

  if resource_env is not None:
    mesh = resource_env.physical_mesh
    api_name = 'pjit'
  else:
    # resource_env is `None` in the jit wrapper around pjit.
    mesh = None
    api_name = 'jit'

  # Convert to `NamedSharding` when `jax_array` is not enabled. This is
  # because GDA/SDA/DA are dependent on mesh for generating outputs.
  # NamedSharding is required for host-local inputs too.
  any_auto = pxla.check_if_any_auto(it.chain(in_shardings,  out_shardings))
  if not config.jax_array or any_auto:
    in_shardings: Tuple[MeshShardingMinusUnspecified, ...] = cast(  # type:ignore[no-redef]
        Tuple[MeshShardingMinusUnspecified, ...], tuple(
            NamedSharding._from_parsed_pspec(
                mesh, parse_flatten_op_sharding(i._op_sharding, mesh)[0]) # type: ignore
            if isinstance(i, GSPMDSharding) else i
            for i in in_shardings
    ))
    out_shardings: Tuple[MeshSharding, ...] = cast(  # type: ignore[no-redef]
        Tuple[MeshSharding, ...], tuple(
            NamedSharding._from_parsed_pspec(
                mesh, parse_flatten_op_sharding(o._op_sharding, mesh)[0]) # type: ignore
            if isinstance(o, GSPMDSharding) else o
            for o in out_shardings
    ))

  # For `pjit(xmap)` cases, it needs to take the `lower_mesh_computation` path
  # because `xmap` only supports SPMDAxisContext right now.
  if any_auto or dispatch.jaxpr_has_primitive(jaxpr.jaxpr, 'xmap'):
    return pxla.lower_mesh_computation(
      jaxpr, api_name, name, mesh,
      in_shardings, out_shardings, donated_invars,
      True, jaxpr.in_avals, tiling_method=None, in_is_global=in_is_global,
      lowering_platform=lowering_platform)
  else:
    return pxla.lower_sharding_computation(
        jaxpr, api_name, name, in_shardings, out_shardings, donated_invars,
        jaxpr.in_avals, in_is_global=in_is_global, keep_unused=keep_unused,
        always_lower=always_lower,
        devices_from_context=(
            None if mesh is None or mesh.empty else list(mesh.devices.flat)),
        lowering_platform=lowering_platform)
