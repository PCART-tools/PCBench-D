@_wraps(np.msort)
def msort(a):
  return sort(a, axis=0)
