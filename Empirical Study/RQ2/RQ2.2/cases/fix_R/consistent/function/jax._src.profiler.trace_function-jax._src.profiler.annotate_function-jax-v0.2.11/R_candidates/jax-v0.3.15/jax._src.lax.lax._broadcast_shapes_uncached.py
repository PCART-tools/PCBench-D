def _broadcast_shapes_uncached(*shapes):
  _validate_shapes(shapes)
  fst, *rst = shapes
  if not rst: return fst

  # First check if we need only rank promotion (and not singleton-broadcasting).
  try: return _reduce(_broadcast_ranks, rst, fst)
  except ValueError: pass

  # Next try singleton-broadcasting, padding out ranks using singletons.
  ndim = _max(len(shape) for shape in shapes)
  shape_list = [(1,) * (ndim - len(shape)) + shape for shape in shapes]
  result_shape = _try_broadcast_shapes(shape_list)
  if result_shape is None:
    raise ValueError("Incompatible shapes for broadcasting: {}"
                     .format(tuple(shape_list)))
  return result_shape
