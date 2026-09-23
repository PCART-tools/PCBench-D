def _dynamic_update_index(x, idx, val):
  if not idx: return val
  ndim = len(x.shape)
  starts = [*idx] + [lax.full_like(idx[0], 0, shape=())] * (ndim - len(idx))
  update = val.reshape((1,) * len(idx) + x.shape[len(idx):])
  return lax.dynamic_update_slice(x, update, starts)
