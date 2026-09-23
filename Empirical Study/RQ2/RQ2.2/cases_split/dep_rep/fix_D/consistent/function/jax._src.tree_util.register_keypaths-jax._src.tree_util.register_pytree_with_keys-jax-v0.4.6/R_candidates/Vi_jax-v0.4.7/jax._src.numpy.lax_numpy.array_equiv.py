@util._wraps(np.array_equiv)
def array_equiv(a1: ArrayLike, a2: ArrayLike) -> Array:
  try:
    a1, a2 = asarray(a1), asarray(a2)
  except Exception:
    return bool_(False)
  try:
    eq = ufuncs.equal(a1, a2)
  except ValueError:
    # shapes are not broadcastable
    return bool_(False)
  return reductions.all(eq)
