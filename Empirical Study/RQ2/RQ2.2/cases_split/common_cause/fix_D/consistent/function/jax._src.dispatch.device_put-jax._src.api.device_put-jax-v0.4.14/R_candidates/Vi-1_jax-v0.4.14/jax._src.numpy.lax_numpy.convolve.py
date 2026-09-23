@util._wraps(np.convolve, lax_description=_PRECISION_DOC,
             extra_params=_PREFERRED_ELEMENT_TYPE_DESCRIPTION)
@partial(jit, static_argnames=('mode', 'precision', 'preferred_element_type'))
def convolve(a: ArrayLike, v: ArrayLike, mode: str = 'full', *,
             precision: PrecisionLike = None,
             preferred_element_type: Optional[dtype] = None) -> Array:
  util.check_arraylike("convolve", a, v)
  return _conv(asarray(a), asarray(v), mode=mode, op='convolve',
               precision=precision, preferred_element_type=preferred_element_type)
