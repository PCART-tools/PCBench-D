@implements(np.floor, module='numpy')
@partial(jit, inline=True)
def floor(x: ArrayLike, /) -> Array:
  check_arraylike('floor', x)
  if dtypes.isdtype(dtypes.dtype(x), ('integral', 'bool')):
    return lax.asarray(x)
  return lax.floor(*promote_args_inexact('floor', x))
