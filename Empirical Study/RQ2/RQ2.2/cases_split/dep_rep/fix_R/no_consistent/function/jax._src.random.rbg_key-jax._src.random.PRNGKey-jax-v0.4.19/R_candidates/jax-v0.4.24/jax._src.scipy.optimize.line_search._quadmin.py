def _quadmin(a, fa, fpa, b, fb):
  D = fa
  C = fpa
  db = b - a
  B = (fb - D - C * db) / (db ** 2)
  xmin = a - C / (2. * B)
  return xmin
