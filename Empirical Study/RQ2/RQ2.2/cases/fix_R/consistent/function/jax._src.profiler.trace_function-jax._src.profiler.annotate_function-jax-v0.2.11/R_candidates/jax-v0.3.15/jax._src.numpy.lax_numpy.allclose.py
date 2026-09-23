@_wraps(np.allclose)
@partial(jit, static_argnames=('equal_nan',))
def allclose(a, b, rtol=1e-05, atol=1e-08, equal_nan=False):
  _check_arraylike("allclose", a, b)
  return all(isclose(a, b, rtol, atol, equal_nan))
