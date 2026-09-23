@_wraps(np.extract)
def extract(condition, arr):
  return compress(ravel(condition), ravel(arr))
