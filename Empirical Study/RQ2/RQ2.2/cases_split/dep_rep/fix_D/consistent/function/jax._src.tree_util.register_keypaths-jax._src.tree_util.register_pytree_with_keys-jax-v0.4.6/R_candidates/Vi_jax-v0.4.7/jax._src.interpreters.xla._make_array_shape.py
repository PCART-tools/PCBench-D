def _make_array_shape(a: ShapedArray) -> Sequence[xc.Shape]:
  if a.dtype == dtypes.float0:
    return (xc.Shape.array_shape(np.dtype('bool'), a.shape),)
  else:
    return (xc.Shape.array_shape(a.dtype, a.shape),)
