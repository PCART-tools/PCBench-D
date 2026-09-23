def _get_sharding_specs(
    shardings: Sequence[sharding_impls.XLACompatibleSharding], avals: Sequence[ShapedArray]
) -> Sequence[ShardingSpec]:
  if all(isinstance(s, sharding_impls.PmapSharding) for s in shardings):
    return [s.sharding_spec for s in shardings]  # type: ignore
  elif all(isinstance(s, sharding_impls.NamedSharding) for s in shardings):
    out = []
    for aval, s in safe_zip(avals, shardings):
      ns = cast(sharding_impls.NamedSharding, s)
      out.append(
          new_mesh_sharding_specs(ns.mesh.shape, ns.mesh.axis_names)(
              aval.ndim, get_array_mapping(ns.spec)
          )
      )
    return out
  else:
    raise ValueError('Getting sharding spec is only supported for '
                     "PmapSharding and NamedSharding, "
                     f"but got {shardings}.")
