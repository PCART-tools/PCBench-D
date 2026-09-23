@_wraps(np.vdot, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('precision',), inline=True)
def vdot(a, b, *, precision=None):
  _check_arraylike("vdot", a, b)
  if issubdtype(_dtype(a), complexfloating):
    a = conj(a)
  return dot(a.ravel(), b.ravel(), precision=precision)
