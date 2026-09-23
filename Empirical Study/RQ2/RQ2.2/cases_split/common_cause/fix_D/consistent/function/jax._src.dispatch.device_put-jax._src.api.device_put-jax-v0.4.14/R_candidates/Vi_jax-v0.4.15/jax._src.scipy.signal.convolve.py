@_wraps(osp_signal.convolve)
def convolve(in1: Array, in2: Array, mode: str = 'full', method: str = 'auto',
             precision: PrecisionLike = None) -> Array:
  if method == 'fft':
    return fftconvolve(in1, in2, mode=mode)
  elif method in ['direct', 'auto']:
    return _convolve_nd(in1, in2, mode, precision=precision)
  else:
    raise ValueError(f"Got {method=}; expected 'auto', 'fft', or 'direct'.")
