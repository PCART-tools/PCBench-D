@_wraps(np.fft.irfft2)
def irfft2(a, s=None, axes=(-2,-1), norm=None):
  return _fft_core_2d('irfft2', xla_client.FftType.IRFFT, a, s=s, axes=axes,
                      norm=norm)
