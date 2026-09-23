def _sda_one_replica_buffer_indices(self):
  """Indices of buffers containing one complete copy of the array data."""
  if self._one_replica_buffer_indices is None:
    self._one_replica_buffer_indices = _one_replica_buffer_indices(self.indices)
  return self._one_replica_buffer_indices
