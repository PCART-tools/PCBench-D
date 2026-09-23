def _jumble_result(axis_size, stacked_axis, ragged_axes, x):
  binder = core.Var(0, '', core.ShapedArray((), np.dtype('int32')))
  if stacked_axis != 0:
    raise NotImplementedError  # TODO Transpose x so the stacked axis is axis 0
  shape = list(x.shape)
  del shape[0]
  for ragged_axis, segment_lens in ragged_axes:
    shape[ragged_axis-1] = IndexedAxisSize(binder, segment_lens)
  elt_ty = core.DShapedArray(tuple(shape), x.dtype, x.weak_type)
  return Jumble(JumbleTy(binder, axis_size, elt_ty), x)
