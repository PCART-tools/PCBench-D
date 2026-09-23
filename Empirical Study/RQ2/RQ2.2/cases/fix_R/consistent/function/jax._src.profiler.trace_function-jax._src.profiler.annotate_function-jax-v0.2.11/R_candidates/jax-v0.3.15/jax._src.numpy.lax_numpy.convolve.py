@_wraps(np.convolve, lax_description=_PRECISION_DOC)
@partial(jit, static_argnames=('mode', 'precision'))
def convolve(a, v, mode='full', *, precision=None):
  _check_arraylike("convolve", a, v)
  return _conv(a, v, mode, 'convolve', precision)
