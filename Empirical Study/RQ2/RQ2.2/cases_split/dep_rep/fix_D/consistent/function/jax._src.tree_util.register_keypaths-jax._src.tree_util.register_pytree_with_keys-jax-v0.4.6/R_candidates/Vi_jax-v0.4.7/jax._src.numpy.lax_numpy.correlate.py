@util._wraps(np.correlate, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('mode', 'precision'))
def correlate(a: ArrayLike, v: ArrayLike, mode: str = 'valid', *,
              precision: PrecisionLike = None) -> Array:
  util.check_arraylike("correlate", a, v)
  return _conv(asarray(a), asarray(v), mode, 'correlate', precision)
