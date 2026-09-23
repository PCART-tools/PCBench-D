def _isEmpty2d(arr):
  # check size first for efficiency
  return arr.size == 0 and np.prod(arr.shape[-2:]) == 0
