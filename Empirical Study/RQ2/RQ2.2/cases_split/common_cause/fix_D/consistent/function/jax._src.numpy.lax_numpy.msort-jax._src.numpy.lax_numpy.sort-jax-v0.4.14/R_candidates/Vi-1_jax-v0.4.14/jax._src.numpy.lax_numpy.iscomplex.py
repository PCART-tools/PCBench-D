@util._wraps(np.iscomplex)
@jit
def iscomplex(x: ArrayLike) -> Array:
  i = ufuncs.imag(x)
  return lax.ne(i, _lax_const(i, 0))
