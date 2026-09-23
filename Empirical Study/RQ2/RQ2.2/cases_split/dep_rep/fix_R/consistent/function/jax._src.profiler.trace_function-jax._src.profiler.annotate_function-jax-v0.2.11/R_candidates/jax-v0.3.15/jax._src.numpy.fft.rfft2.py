@_wraps(np.fft.rfft2)
def rfft2(a, s=None, axes=(-2,-1), norm=None):
  return _fft_core_2d('rfft2', xla_client.FftType.RFFT, a, s=s, axes=axes,
                      norm=norm)
