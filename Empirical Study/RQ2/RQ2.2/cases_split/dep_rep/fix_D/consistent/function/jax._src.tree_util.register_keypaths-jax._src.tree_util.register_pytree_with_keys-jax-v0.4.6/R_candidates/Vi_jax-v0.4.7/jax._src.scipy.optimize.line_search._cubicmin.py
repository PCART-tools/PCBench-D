def _cubicmin(a, fa, fpa, b, fb, c, fc):
  dtype = jnp.result_type(a, fa, fpa, b, fb, c, fc)
  C = fpa
  db = b - a
  dc = c - a
  denom = (db * dc) ** 2 * (db - dc)
  d1 = jnp.array([[dc ** 2, -db ** 2],
                  [-dc ** 3, db ** 3]], dtype=dtype)
  d2 = jnp.array([fb - fa - C * db, fc - fa - C * dc], dtype=dtype)
  A, B = _dot(d1, d2) / denom

  radical = B * B - 3. * A * C
  xmin = a + (-B + jnp.sqrt(radical)) / (3. * A)

  return xmin
