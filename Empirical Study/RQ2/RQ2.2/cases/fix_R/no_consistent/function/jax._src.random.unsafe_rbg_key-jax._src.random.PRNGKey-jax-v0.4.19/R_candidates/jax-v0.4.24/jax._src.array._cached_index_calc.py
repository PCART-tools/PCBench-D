@functools.lru_cache(maxsize=4096)
def _cached_index_calc(s, shape):
  map_ = s.addressable_devices_indices_map(shape)
  seen_h_indices = set()
  m = {}
  for d, index in map_.items():
    h_index = hashed_index(index)
    if h_index not in seen_h_indices:
      seen_h_indices.add(h_index)
      m[d] = index
  return m
