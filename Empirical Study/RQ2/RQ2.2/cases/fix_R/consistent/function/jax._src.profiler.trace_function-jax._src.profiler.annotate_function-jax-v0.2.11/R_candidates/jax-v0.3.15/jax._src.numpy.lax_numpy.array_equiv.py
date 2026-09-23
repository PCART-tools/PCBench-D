@_wraps(np.array_equiv)
def array_equiv(a1, a2):
  try:
    a1, a2 = asarray(a1), asarray(a2)
  except Exception:
    return False
  try:
    eq = equal(a1, a2)
  except ValueError:
    # shapes are not broadcastable
    return False
  return all(eq)
