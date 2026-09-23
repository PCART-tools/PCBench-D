@util._wraps(np.allclose)
@partial(jit, static_argnames=('equal_nan',))
def allclose(a: ArrayLike, b: ArrayLike, rtol: ArrayLike = 1e-05,
             atol: ArrayLike = 1e-08, equal_nan: bool = False) -> Array:
  util.check_arraylike("allclose", a, b)
  return reductions.all(isclose(a, b, rtol, atol, equal_nan))
