@implements(np.ceil, module='numpy')
@partial(jit, inline=True)
def ceil(x: ArrayLike, /) -> Array:
  check_arraylike('ceil', x)
  if dtypes.isdtype(dtypes.dtype(x), ('integral', 'bool')):
    return lax.asarray(x)
  return lax.ceil(*promote_args_inexact('ceil', x))
