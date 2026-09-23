@implements(np.real)
@partial(jit, inline=True)
def real(val: ArrayLike, /) -> Array:
  check_arraylike("real", val)
  return lax.real(val) if np.iscomplexobj(val) else lax.asarray(val)
