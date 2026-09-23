def _scatter_dimensions_proto(
    indices_shape: Sequence[int], dimension_numbers: ScatterDimensionNumbers
) -> xla_client.ScatterDimensionNumbers:
  assert type(dimension_numbers) is ScatterDimensionNumbers
  proto = xla_client.ScatterDimensionNumbers()
  proto.update_window_dims.extend(dimension_numbers.update_window_dims)
  proto.inserted_window_dims.extend(dimension_numbers.inserted_window_dims)
  proto.scatter_dims_to_operand_dims.extend(
      dimension_numbers.scatter_dims_to_operand_dims)
  assert len(indices_shape) > 0, indices_shape
  proto.index_vector_dim = len(indices_shape) - 1
  return proto
