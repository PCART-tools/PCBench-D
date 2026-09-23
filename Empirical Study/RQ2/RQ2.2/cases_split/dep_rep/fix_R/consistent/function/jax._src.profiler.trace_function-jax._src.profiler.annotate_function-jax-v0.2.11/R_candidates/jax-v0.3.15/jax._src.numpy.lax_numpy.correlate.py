@_wraps(np.correlate, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('mode', 'precision'))
def correlate(a, v, mode='valid', *, precision=None):
  _check_arraylike("correlate", a, v)
  return _conv(a, v, mode, 'correlate', precision)
