@_wraps(np.trunc, module='numpy')
@jit
def trunc(x):
  _check_arraylike('trunc', x)
  return where(lax.lt(x, _lax_const(x, 0)), ceil(x), floor(x))
