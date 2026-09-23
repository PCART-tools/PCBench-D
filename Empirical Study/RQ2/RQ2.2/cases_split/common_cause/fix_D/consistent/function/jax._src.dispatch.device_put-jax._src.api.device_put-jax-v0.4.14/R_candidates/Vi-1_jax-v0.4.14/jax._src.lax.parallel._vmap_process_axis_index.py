def _vmap_process_axis_index(self, frame):
  assert frame.size is not None
  return batching.BatchTracer(self, lax.iota(np.int32, frame.size), 0)
