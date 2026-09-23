def _get_sharding_specs(
    shardings: Sequence[sharding_internal.XLACompatibleSharding], avals: Sequence[ShapedArray]
) -> Sequence[ShardingSpec]:
  if all(isinstance(s, sharding_internal.PmapSharding) for s in shardings):
    return [s.sharding_spec for s in shardings]  # type: ignore
  elif all(isinstance(s, sharding_internal.NamedSharding) for s in shardings):
    return [new_mesh_sharding_specs(s.mesh.shape, s.mesh.axis_names)(
              aval.ndim, get_array_mapping(s.spec))
            for aval, s in safe_zip(avals, shardings)]
  else:
    raise ValueError('Getting sharding spec is only supported for '
                     "PmapSharding and NamedSharding, "
                     f"but got {shardings}.")
