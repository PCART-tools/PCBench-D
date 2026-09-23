@util.implements(np.vdot, lax_description=_PRECISION_DOC,
                 extra_params=_DOT_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def vdot(
    a: ArrayLike, b: ArrayLike, *,
    precision: PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
) -> Array:
  util.check_arraylike("vdot", a, b)
  if issubdtype(_dtype(a), complexfloating):
    a = ufuncs.conj(a)
  return dot(ravel(a), ravel(b), precision=precision,
             preferred_element_type=preferred_element_type)
