@util._wraps(np.extract)
def extract(condition: ArrayLike, arr: ArrayLike) -> Array:
  return compress(ravel(condition), ravel(arr))
