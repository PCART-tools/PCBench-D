def _pgather_abstract_eval(src, idx, *, axes):
  # TODO: Avals with names rule: remove all axes from src, insert those from idx
  #       The order is important, because it is ok to re-insert one of the deleted axes!
  shape = list(src.shape)
  for axis in sorted((a for a in axes if isinstance(a, int)), reverse=True):
    del shape[axis]
  shape = idx.shape + tuple(shape)
  return ShapedArray(shape, src.dtype)
