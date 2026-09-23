def _swap_discharge(x, val, idx, indexed_dims):
  if not any(indexed_dims):
    z, x_new = x, val
  elif all(not i.shape for i in idx):
    z = _dynamic_index(x, idx, indexed_dims)
    x_new = _dynamic_update_index(x, idx, val, indexed_dims)
  else:
    z = _prepend_gather(x, idx, indexed_dims)
    x_new = _prepend_scatter(x, idx, indexed_dims, val)
  return z, x_new
