@util.implements(np.correlate, lax_description=_PRECISION_DOC,
                 extra_params=_CONV_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
@partial(jit, static_argnames=('mode', 'precision', 'preferred_element_type'))
def correlate(a: ArrayLike, v: ArrayLike, mode: str = 'valid', *,
              precision: PrecisionLike = None,
              preferred_element_type: dtype | None = None) -> Array:
  util.check_arraylike("correlate", a, v)
  return _conv(asarray(a), asarray(v), mode=mode, op='correlate',
               precision=precision, preferred_element_type=preferred_element_type)
