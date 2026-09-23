def _is_valid_integer_index_for_slice(idx, size, mode):
  if size == 0:
    return False
  if _is_integer_index(idx):
    return -size <= idx < size
  try:
    shape, dtype = np.shape(idx), _dtype(idx)
  except:
    return False
  if shape == () and np.issubdtype(dtype, np.integer):
    # For dynamic integer indices, dynamic_slice semantics require index clipping:
    return mode in [None, 'promise_inbounds', 'clip']
  return False
