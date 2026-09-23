@_wraps(np.tril_indices_from)
def tril_indices_from(arr, k=0):
  return tril_indices(arr.shape[-2], k=k, m=arr.shape[-1])
