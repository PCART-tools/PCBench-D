@util._wraps(np.inner, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('precision',), inline=True)
def inner(a, b, *, precision=None):
  if ndim(a) == 0 or ndim(b) == 0:
    return a * b
  return tensordot(a, b, (-1, -1), precision=precision)
