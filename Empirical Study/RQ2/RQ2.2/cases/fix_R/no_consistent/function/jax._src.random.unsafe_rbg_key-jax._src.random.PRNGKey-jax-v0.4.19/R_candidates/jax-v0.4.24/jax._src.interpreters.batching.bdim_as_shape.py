def bdim_as_shape(
    bdim: int | RaggedAxis, data_shape: core.Shape) -> core.Shape:
  if isinstance(bdim, RaggedAxis):
    result = list(data_shape)
    binder = core.Var(0, '', core.ShapedArray((), np.dtype('int32')))
    for ragged_axis, segment_lens in bdim.ragged_axes:
      result[ragged_axis] = IndexedAxisSize(binder, segment_lens)
    return tuple(result)
  else:
    return data_shape
