def _pile_result(axis_size, axis, segment_lens, x):
  binder = core.Var(0, '', core.ShapedArray((), np.dtype('int32')))
  shape = list(x.shape)
  shape[axis] = IndexedAxisSize(binder, segment_lens)
  elt_ty = core.DShapedArray(tuple(shape), x.dtype, x.weak_type)
  return Pile(PileTy(binder, axis_size, elt_ty), x)
