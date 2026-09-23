def _is_singleton_reshape(old, new):
  # A singleton reshape is one where only singleton dimensions are added. We
  # want to detect them because they can be expressed as (lazy) broadcasts.
  old, new = iter(old), iter(new)
  d1, d2 = next(old, None), next(new, None)
  bcast_dims = []
  i = 0
  while True:
    if d1 is d2 is None:
      return bcast_dims
    elif d1 == d2:
      bcast_dims.append(i)
      i += 1
      d1, d2 = next(old, None), next(new, None)
    elif d2 == 1:
      i += 1
      d2 = next(new, None)
    else:
      return None
