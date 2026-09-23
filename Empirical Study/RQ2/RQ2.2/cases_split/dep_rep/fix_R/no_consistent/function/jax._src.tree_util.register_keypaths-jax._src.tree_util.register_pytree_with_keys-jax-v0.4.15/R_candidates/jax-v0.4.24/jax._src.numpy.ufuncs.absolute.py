@implements(np.absolute, module='numpy')
@partial(jit, inline=True)
def absolute(x: ArrayLike, /) -> Array:
  check_arraylike('absolute', x)
  dt = dtypes.dtype(x)
  return lax.asarray(x) if dt == np.bool_ or dtypes.issubdtype(dt, np.unsignedinteger) else lax.abs(x)
