@util._wraps(np.diag_indices_from)
def diag_indices_from(arr):
  util.check_arraylike("diag_indices_from", arr)
  if not arr.ndim >= 2:
    raise ValueError("input array must be at least 2-d")

  if len(set(arr.shape)) != 1:
    raise ValueError("All dimensions of input must be of equal length")

  return diag_indices(arr.shape[0], ndim=arr.ndim)
