def _pack_indices(non_slice_idx, indexed_dims):
  non_slice_idx_iter = iter(non_slice_idx)
  return tuple(
      next(non_slice_idx_iter) if indexed else slice(None)
      for indexed in indexed_dims
  )
