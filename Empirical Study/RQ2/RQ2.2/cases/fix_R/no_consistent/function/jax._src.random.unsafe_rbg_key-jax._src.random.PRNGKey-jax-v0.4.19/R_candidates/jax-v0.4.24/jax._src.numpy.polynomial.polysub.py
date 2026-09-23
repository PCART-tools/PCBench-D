@implements(np.polysub)
@jit
def polysub(a1: Array, a2: Array) -> Array:
  check_arraylike("polysub", a1, a2)
  a1, a2 = promote_dtypes(a1, a2)
  return polyadd(a1, -a2)
