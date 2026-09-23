@_wraps(np.imag)
@partial(jit, inline=True)
def imag(val: ArrayLike, /) -> Array:
  _check_arraylike("imag", val)
  return lax.imag(val) if np.iscomplexobj(val) else lax.full_like(val, 0)
