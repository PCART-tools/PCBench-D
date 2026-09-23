def _fft_core_1d(func_name, fft_type, a, n, axis, norm):
  _axis_check_1d(func_name, axis)
  axes = None if axis is None else [axis]
  s = None if n is None else [n]
  return _fft_core(func_name, fft_type, a, s, axes, norm)
