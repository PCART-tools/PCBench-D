def _try_broadcast_shapes(
    shapes: Sequence[tuple[int, ...]]) -> tuple[int, ...] | None:
  if len(shapes) == 1: return shapes[0]
  ranks = {len(shape) for shape in shapes}
  if len(ranks) > 1: return None  # must have consistent rank
  rank = ranks.pop()
  if not rank: return ()  # scalar case
  result_shape = []
  for ds in unsafe_zip(*shapes):
    if all(core.same_referent(d, ds[0]) for d in ds[1:]):
      # if all axes are identical objects, the resulting size is the object
      result_shape.append(ds[0])
    else:
      # if all dims are equal (or 1), the result is the non-1 size (or 1)
      non_1s = [d for d in ds if not core.definitely_equal(d, 1)]
      if not non_1s:
        result_shape.append(1)
      elif all(core.definitely_equal(non_1s[0], d) for d in non_1s[1:]):
        result_shape.append(non_1s[0])
      else:
        return None
  return tuple(result_shape)
