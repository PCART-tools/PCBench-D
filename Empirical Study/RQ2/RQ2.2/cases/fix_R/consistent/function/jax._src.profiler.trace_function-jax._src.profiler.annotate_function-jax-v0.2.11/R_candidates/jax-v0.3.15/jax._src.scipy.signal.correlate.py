@_wraps(osp_signal.correlate)
def correlate(in1, in2, mode='full', method='auto',
              precision=None):
  if method != 'auto':
    warnings.warn("correlate() ignores method argument")
  return _convolve_nd(in1, jnp.flip(in2.conj()), mode, precision=precision)
