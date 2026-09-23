@util.implements(np.inner, lax_description=_PRECISION_DOC,
                 extra_params=_DOT_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
@partial(jit, static_argnames=('precision', 'preferred_element_type'), inline=True)
def inner(
    a: ArrayLike, b: ArrayLike, *, precision: PrecisionLike = None,
    preferred_element_type: DType | None = None,
) -> Array:
  # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
  util.check_arraylike("inner", a, b, emit_warning=True)
  if ndim(a) == 0 or ndim(b) == 0:
    a = asarray(a, dtype=preferred_element_type)
    b = asarray(b, dtype=preferred_element_type)
    return a * b
  return tensordot(a, b, (-1, -1), precision=precision,
                   preferred_element_type=preferred_element_type)
