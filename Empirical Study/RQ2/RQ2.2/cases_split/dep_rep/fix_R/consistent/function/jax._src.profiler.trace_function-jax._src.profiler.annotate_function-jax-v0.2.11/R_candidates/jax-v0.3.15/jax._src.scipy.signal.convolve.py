@_wraps(osp_signal.convolve)
def convolve(in1, in2, mode='full', method='auto',
             precision=None):
  if method != 'auto':
    warnings.warn("convolve() ignores method argument")
  return _convolve_nd(in1, in2, mode, precision=precision)
