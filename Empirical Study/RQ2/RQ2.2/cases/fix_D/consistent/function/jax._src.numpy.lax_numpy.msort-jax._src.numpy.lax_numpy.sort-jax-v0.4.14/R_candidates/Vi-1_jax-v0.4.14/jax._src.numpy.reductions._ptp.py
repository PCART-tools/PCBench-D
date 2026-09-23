@partial(api.jit, static_argnames=('axis', 'keepdims'))
def _ptp(a: ArrayLike, axis: Axis = None, out: None = None,
         keepdims: bool = False) -> Array:
  check_arraylike("ptp", a)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.ptp is not supported.")
  x = amax(a, axis=axis, keepdims=keepdims)
  y = amin(a, axis=axis, keepdims=keepdims)
  return lax.sub(x, y)
