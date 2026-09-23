def _dynamic_index(x, idx, indexed_dims):
  assert isinstance(idx, (list, tuple)) and idx
  idx_ = iter(idx)
  starts = [next(idx_) if b else np.int32(0) for b in indexed_dims]
  assert next(idx_, None) is None
  sizes = [1 if b else size for b, size in zip(indexed_dims, x.shape)]
  out = lax_slicing.dynamic_slice(x, starts, sizes)
  return lax.squeeze(out, [i for i, b in enumerate(indexed_dims) if b])
