def _create_copy_plan(arrays, s: Sharding, shape: Shape):
  di_map = _cached_index_calc(s, shape)
  copy_plan = []
  for a in arrays:
    ind = di_map.get(a.device(), None)
    if ind is not None:
      copy_plan.append((ind, a))
  return copy_plan
