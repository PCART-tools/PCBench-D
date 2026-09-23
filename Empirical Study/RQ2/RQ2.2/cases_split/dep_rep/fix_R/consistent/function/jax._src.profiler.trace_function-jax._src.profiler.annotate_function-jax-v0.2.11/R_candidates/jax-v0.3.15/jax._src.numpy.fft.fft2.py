@_wraps(np.fft.fft2)
def fft2(a, s=None, axes=(-2,-1), norm=None):
  return _fft_core_2d('fft2', xla_client.FftType.FFT, a, s=s, axes=axes,
                      norm=norm)
