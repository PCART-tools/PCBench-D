def parse_flatten_op_sharding(op_sharding: xc.OpSharding | xc.HloSharding,
                              mesh: mesh_lib.Mesh) -> Sequence[ParsedPartitionSpec]:
  if isinstance(op_sharding, xc.HloSharding):
    op_sharding = op_sharding.to_proto()  # type: ignore
  if op_sharding.type == xc.OpSharding.Type.TUPLE:
    out: list[ParsedPartitionSpec] = []
    for s in op_sharding.tuple_shardings:
      out.extend(parse_flatten_op_sharding(s, mesh))
    return out
  elif op_sharding.type == xc.OpSharding.Type.REPLICATED:
    return [CanonicalizedParsedPartitionSpec(
        ParsedPartitionSpec(PartitionSpec(), ()))]
  elif op_sharding.type == xc.OpSharding.Type.OTHER:
    mesh_shape = mesh.shape
    mesh_axis_order = unflatten_array(mesh.shape, op_sharding.tile_assignment_devices)
    mesh_axis = iter(mesh_axis_order)
    shape = op_sharding.tile_assignment_dimensions
    partitions = []
    for dim_size in shape:
      dim_partitions = []
      while dim_size > 1:
        axis = next(mesh_axis)
        axis_size = mesh_shape[axis]
        assert dim_size % axis_size == 0
        dim_size //= axis_size
        dim_partitions.append(axis)
      partitions.append(tuple(dim_partitions))
    if op_sharding.last_tile_dims == [xc.OpSharding.Type.REPLICATED]:
      replicate_on_last_tile_dim = True
    else:
      replicate_on_last_tile_dim = op_sharding.replicate_on_last_tile_dim
      if op_sharding.last_tile_dims:
        raise NotImplementedError("Unhandled OpSharding type. Please open a bug report!")
    if replicate_on_last_tile_dim:
      partitions = partitions[:-1]
    return [CanonicalizedParsedPartitionSpec(
        ParsedPartitionSpec('<internally generated spec>', partitions))]
  else:
    raise AssertionError("Unhandled OpSharding type. Please open a bug report!")
