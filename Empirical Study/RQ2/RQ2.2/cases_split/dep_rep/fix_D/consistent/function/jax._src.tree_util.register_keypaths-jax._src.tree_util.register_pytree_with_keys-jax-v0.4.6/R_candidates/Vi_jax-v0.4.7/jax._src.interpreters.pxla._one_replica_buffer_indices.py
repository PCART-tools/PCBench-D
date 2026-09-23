def _one_replica_buffer_indices(indices: Tuple[Index, ...]):
  """Returns a set of buffer-indices containing one complete copy of the array."""
  one_replica_indices = []
  seen_index_hashes = set()
  for i, index in enumerate(indices):
    hashed_index = _hashable_index(index)
    if hashed_index not in seen_index_hashes:
      one_replica_indices.append(i)
      seen_index_hashes.add(hashed_index)
  return one_replica_indices
