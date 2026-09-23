@_wraps(np.real)
@partial(jit, inline=True)
def real(val: ArrayLike, /) -> Array:
  _check_arraylike("real", val)
  return lax.real(val) if np.iscomplexobj(val) else _asarray(val)
