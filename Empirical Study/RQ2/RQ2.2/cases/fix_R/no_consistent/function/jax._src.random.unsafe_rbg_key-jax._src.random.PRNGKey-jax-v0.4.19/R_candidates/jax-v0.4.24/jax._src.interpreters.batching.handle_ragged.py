def handle_ragged(in_avals: list[core.AbstractValue], dim: RaggedAxis,
                  aval: core.ShapedArray) -> tuple[int, core.ShapedArray]:
  new_shape = list(aval.shape)
  for i, dbi in dim.ragged_axes:
    new_shape[i - (dim.stacked_axis < i)] = in_avals[dbi.val].dtype.bound
  new_aval = aval.update(shape=tuple(new_shape))
  return dim.stacked_axis, new_aval
