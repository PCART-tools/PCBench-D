def _get_discharge(x, idx, indexed_dims):
  if not any(indexed_dims):
    return x
  if all(not i.shape for i in idx):
    return _dynamic_index(x, idx, indexed_dims)
  else:
    return _prepend_gather(x, idx, indexed_dims)
