@_wraps(np.array_equal)
def array_equal(a1, a2, equal_nan=False):
  try:
    a1, a2 = asarray(a1), asarray(a2)
  except Exception:
    return False
  if shape(a1) != shape(a2):
    return False
  eq = asarray(a1 == a2)
  if equal_nan:
    eq = logical_or(eq, logical_and(isnan(a1), isnan(a2)))
  return all(eq)
