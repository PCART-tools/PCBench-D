@_wraps(np.triu_indices_from)
def triu_indices_from(arr, k=0):
  return triu_indices(arr.shape[-2], k=k, m=arr.shape[-1])
