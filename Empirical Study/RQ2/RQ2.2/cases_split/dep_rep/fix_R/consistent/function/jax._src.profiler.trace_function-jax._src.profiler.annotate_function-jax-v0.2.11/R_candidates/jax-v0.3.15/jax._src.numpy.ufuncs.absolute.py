@_wraps(np.absolute, module='numpy')
@partial(jit, inline=True)
def absolute(x):
  _check_arraylike('absolute', x)
  dt = dtypes.dtype(x)
  return x if dt == np.bool_ or dtypes.issubdtype(dt, np.unsignedinteger) else lax.abs(x)
