def _triu_size(n, m, k):
  if k < 0:
    return n * m - _triu_size(m, n, (1 - k))
  elif k >= m:
    return 0
  else:
    mk = _min(n, m - k)
    return mk * (mk + 1) // 2 + mk * (m - k - mk)
