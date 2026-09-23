def _addupdate_discharge(x, val, idx, indexed_dims):
  if not any(indexed_dims):
    return x + val
  if all(not i.shape for i in idx):
    y = val + _dynamic_index(x, idx, indexed_dims)
    return _dynamic_update_index(x, idx, y, indexed_dims)
  else:
    return _prepend_scatter(x, idx, indexed_dims, val, add=True)
