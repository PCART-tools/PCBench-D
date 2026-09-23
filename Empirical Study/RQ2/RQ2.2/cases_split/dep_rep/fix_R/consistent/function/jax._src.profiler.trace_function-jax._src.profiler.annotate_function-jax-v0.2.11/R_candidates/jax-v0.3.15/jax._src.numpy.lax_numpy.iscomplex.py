@_wraps(np.iscomplex)
@jit
def iscomplex(x):
  i = imag(x)
  return lax.ne(i, _lax_const(i, 0))
