def _gather_dimensions_proto(
    indices_shape: Sequence[int], dimension_numbers: GatherDimensionNumbers
) -> xla_client.GatherDimensionNumbers:
  assert type(dimension_numbers) is GatherDimensionNumbers
  proto = xla_client.GatherDimensionNumbers()
  proto.offset_dims.extend(dimension_numbers.offset_dims)
  proto.collapsed_slice_dims.extend(dimension_numbers.collapsed_slice_dims)
  proto.start_index_map.extend(dimension_numbers.start_index_map)
  assert len(indices_shape) > 0, indices_shape
  proto.index_vector_dim = len(indices_shape) - 1
  return proto
