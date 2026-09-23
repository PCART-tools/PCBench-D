@_wraps(np.conjugate, module='numpy')
@partial(jit, inline=True)
def conjugate(x: ArrayLike, /) -> Array:
  check_arraylike("conjugate", x)
  return lax.conj(x) if np.iscomplexobj(x) else _asarray(x)
