@util._wraps(np.convolve, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('mode', 'precision'))
def convolve(a: ArrayLike, v: ArrayLike, mode: str = 'full', *,
             precision: PrecisionLike = None) -> Array:
  util._check_arraylike("convolve", a, v)
  return _conv(asarray(a), asarray(v), mode, 'convolve', precision)
