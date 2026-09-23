@util._wraps(np.array_equal)
def array_equal(a1: ArrayLike, a2: ArrayLike, equal_nan: bool = False) -> Array:
  try:
    a1, a2 = asarray(a1), asarray(a2)
  except Exception:
    return bool_(False)
  if shape(a1) != shape(a2):
    return bool_(False)
  eq = asarray(a1 == a2)
  if equal_nan:
    eq = ufuncs.logical_or(eq, ufuncs.logical_and(ufuncs.isnan(a1), ufuncs.isnan(a2)))
  return reductions.all(eq)
