@util._wraps(np.vdot, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('precision',), inline=True)
def vdot(
    a: ArrayLike, b: ArrayLike, *, precision: PrecisionLike = None
) -> Array:
  util.check_arraylike("vdot", a, b)
  if issubdtype(_dtype(a), complexfloating):
    a = ufuncs.conj(a)
  return dot(ravel(a), ravel(b), precision=precision)
