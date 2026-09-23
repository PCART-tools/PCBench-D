@_wraps(np.isreal)
@jit
def isreal(x):
  i = imag(x)
  return lax.eq(i, _lax_const(i, 0))
