def shape_as_bdim(
    stacked_axis: int, data_shape: core.Shape) -> int | RaggedAxis:
  # This assumes that there is only one binder in the data_shape.
  ragged_axes = [(i, size.lengths) for i, size in enumerate(data_shape)
                 if isinstance(size, IndexedAxisSize)]
  return make_batch_axis(len(data_shape), stacked_axis, ragged_axes)
