@weakref_lru_cache
def _pjit_lower_cached(
    jaxpr: core.ClosedJaxpr,
    sdat_in_shardings: SameDeviceAssignmentTuple,
    sdat_out_shardings: SameDeviceAssignmentTuple,
    resource_env,
    donated_invars,
    name: str,
    keep_unused: bool,
    inline: bool,
    always_lower: bool,
    *,
    lowering_platform: Optional[str],
    override_lowering_rules: Optional[
        tuple[tuple[core.Primitive, mlir.LoweringRule]]] = None):
  in_shardings: tuple[PjitShardingMinusUnspecified, ...] = cast(
      tuple[PjitShardingMinusUnspecified, ...], sdat_in_shardings.shardings)
  out_shardings: tuple[PjitSharding, ...] = sdat_out_shardings.shardings

  if resource_env is not None:
    pxla.resource_typecheck(jaxpr, resource_env, {}, lambda: "pjit")

  if resource_env is not None:
    mesh = resource_env.physical_mesh
    api_name = 'pjit'
  else:
    # resource_env is `None` in the jit wrapper around pjit.
    mesh = None
    api_name = 'jit'

  # For `pjit(xmap)` cases, it needs to take the `lower_mesh_computation` path
  # because `xmap` only supports SPMDAxisContext right now.
  if dispatch.jaxpr_has_primitive(jaxpr.jaxpr, 'xmap'):
    return pxla.lower_mesh_computation(
      jaxpr, api_name, name, mesh,
      in_shardings, out_shardings, donated_invars,
      True, jaxpr.in_avals, tiling_method=None,
      lowering_platform=lowering_platform)
  else:
    return pxla.lower_sharding_computation(
        jaxpr, api_name, name, in_shardings, out_shardings,
        tuple(donated_invars), tuple(jaxpr.in_avals),
        keep_unused=keep_unused, inline=inline, always_lower=always_lower,
        devices_from_context=(
            None if mesh is None or mesh.empty else list(mesh.devices.flat)),
        lowering_platform=lowering_platform,
        override_lowering_rules=override_lowering_rules,
)
