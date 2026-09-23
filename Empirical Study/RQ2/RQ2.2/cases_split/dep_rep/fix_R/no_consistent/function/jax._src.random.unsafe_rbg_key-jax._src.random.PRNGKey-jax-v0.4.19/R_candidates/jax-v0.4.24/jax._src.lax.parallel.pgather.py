def pgather(src, idx, axes: int | AxisName):
  """Uses the last positional axis of idx to index into src's axes."""
  if not isinstance(axes, (tuple, list)):
    axes = (axes,)
  # TODO: Canonicalize exes!
  return pgather_p.bind(src, idx, axes=tuple(axes))
