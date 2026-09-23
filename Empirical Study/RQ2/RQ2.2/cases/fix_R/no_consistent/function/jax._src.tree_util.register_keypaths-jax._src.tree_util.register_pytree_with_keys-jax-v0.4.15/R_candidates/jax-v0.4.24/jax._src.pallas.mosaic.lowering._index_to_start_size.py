def _index_to_start_size(idx: tuple[indexing.Slice | int | ir.Value],
                         cast_to_index: bool) -> tuple[ir.Value, int, bool]:
  assert not isinstance(idx, slice)
  if isinstance(idx, indexing.Slice):
    start = _maybe_cast_to_index(cast_to_index, idx.start)
    size = idx.size
    squeeze = False
  elif isinstance(idx, int):
    start = _maybe_cast_to_index(cast_to_index, idx)
    size = 1
    squeeze = True
  else:
    if np.shape(idx):
      raise ValueError(f"Can only use ()-shaped and slice indexing: {idx}")
    start = _maybe_cast_to_index(cast_to_index, idx)
    size = 1
    squeeze = True
  return start, size, squeeze
