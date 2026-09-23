@_wraps(np.swapaxes, lax_description=_ARRAY_VIEW_DOC)
@partial(jit, static_argnames=('axis1', 'axis2'), inline=True)
def swapaxes(a, axis1: int, axis2: int):
  _check_arraylike("swapaxes", a)
  perm = np.arange(ndim(a))
  perm[axis1], perm[axis2] = perm[axis2], perm[axis1]
  return lax.transpose(a, list(perm))
