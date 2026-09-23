@functools.lru_cache(maxsize=4096)
def _process_has_full_value_in_mcjax(s, shape):
  # Return False for single host as a fast path.
  if jax.process_count() == 1:
    return False

  num_unique_indices = len(
      set(hashed_index(v) for v in s.devices_indices_map(shape).values()))
  num_addressable_unique_indices = len(
      set(hashed_index(v) for v in s.addressable_devices_indices_map(shape).values()))
  return num_unique_indices == num_addressable_unique_indices
