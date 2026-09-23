@_wraps(np.polyadd)
@jit
def polyadd(a1, a2):
  _check_arraylike("polyadd", a1, a2)
  a1, a2 = _promote_dtypes(a1, a2)
  if a2.shape[0] <= a1.shape[0]:
    return a1.at[-a2.shape[0]:].add(a2)
  else:
    return a2.at[-a1.shape[0]:].add(a1)
