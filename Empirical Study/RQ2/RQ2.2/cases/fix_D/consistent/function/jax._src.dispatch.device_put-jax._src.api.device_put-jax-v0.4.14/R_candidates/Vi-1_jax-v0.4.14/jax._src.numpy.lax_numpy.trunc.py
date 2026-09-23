@util._wraps(np.trunc, module='numpy')
@jit
def trunc(x: ArrayLike) -> Array:
  util.check_arraylike('trunc', x)
  return where(lax.lt(x, _lax_const(x, 0)), ufuncs.ceil(x), ufuncs.floor(x))
