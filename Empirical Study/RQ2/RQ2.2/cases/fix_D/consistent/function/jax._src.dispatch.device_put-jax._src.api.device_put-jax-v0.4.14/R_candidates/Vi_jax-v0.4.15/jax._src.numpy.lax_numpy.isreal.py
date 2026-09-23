@util._wraps(np.isreal)
@jit
def isreal(x: ArrayLike) -> Array:
  i = ufuncs.imag(x)
  return lax.eq(i, _lax_const(i, 0))
