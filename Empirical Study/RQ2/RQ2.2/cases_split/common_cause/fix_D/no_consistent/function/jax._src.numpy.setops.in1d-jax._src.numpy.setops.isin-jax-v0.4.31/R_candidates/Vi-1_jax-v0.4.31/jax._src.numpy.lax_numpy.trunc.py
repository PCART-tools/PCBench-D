@util.implements(np.trunc, module='numpy')
@jit
def trunc(x: ArrayLike) -> Array:
  util.check_arraylike('trunc', x)
  if dtypes.isdtype(dtypes.dtype(x), ('integral', 'bool')):
    return lax_internal.asarray(x)
  return where(lax.lt(x, _lax_const(x, 0)), ufuncs.ceil(x), ufuncs.floor(x))
