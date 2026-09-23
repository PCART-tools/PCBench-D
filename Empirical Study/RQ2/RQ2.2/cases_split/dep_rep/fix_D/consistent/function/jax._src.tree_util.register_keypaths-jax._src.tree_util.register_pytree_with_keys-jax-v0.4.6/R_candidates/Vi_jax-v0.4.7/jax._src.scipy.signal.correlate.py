@_wraps(osp_signal.correlate)
def correlate(in1: Array, in2: Array, mode: str = 'full', method: str = 'auto',
              precision: PrecisionLike = None) -> Array:
  if method != 'auto':
    warnings.warn("correlate() ignores method argument")
  return _convolve_nd(in1, jnp.flip(in2.conj()), mode, precision=precision)
