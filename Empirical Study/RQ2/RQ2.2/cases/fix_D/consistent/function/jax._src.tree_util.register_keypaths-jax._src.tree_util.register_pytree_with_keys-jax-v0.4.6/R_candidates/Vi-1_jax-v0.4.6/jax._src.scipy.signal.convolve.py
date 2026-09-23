@_wraps(osp_signal.convolve)
def convolve(in1: Array, in2: Array, mode: str = 'full', method: str = 'auto',
             precision: PrecisionLike = None) -> Array:
  if method != 'auto':
    warnings.warn("convolve() ignores method argument")
  return _convolve_nd(in1, in2, mode, precision=precision)
