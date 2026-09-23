def _dynamic_index(x, idx):
  if not idx: return x
  ndim = len(x.shape)
  starts = [*idx] + [lax.full_like(idx[0], 0, shape=())] * (ndim - len(idx))
  sizes = (1,) * len(idx) + x.shape[len(idx):]
  out = lax.dynamic_slice(x, starts, sizes)
  return out.reshape(x.shape[len(idx):])
